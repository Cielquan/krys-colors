#!/usr/bin/env python3
"""Script to validate grammar against GDScript source.

Script will:
- git clone godot source repo
- extract global methods, constants, etc. from godot XML files
- extract marked regexes from grammar file
- check for missing matches in grammar regexes
"""

import json
import logging
import pathlib
import re
import subprocess
import sys
import tempfile
import typing as t
import xml.etree.ElementTree as ET

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

ext_dir = pathlib.Path(__file__).parent / ".."
grammar_file = ext_dir / "syntaxes/gdscript.tmLanguage.yaml"
out_file = ext_dir / "missing-grammar-values.bak.json"


GLOBALS_SOURCE_FILES = (
    pathlib.Path("modules/gdscript/doc_classes/@GDScript.xml"),
    pathlib.Path("doc/classes/@GlobalScope.xml"),
)

type Category = t.Literal[
    "const",
    "meth",
    "enum",
    "const-deprecated",
    "meth-deprecated",
    "class",
    "virtual",
]
CATEGORIES: list[Category] = [
    "const",
    "meth",
    "enum",
    "const-deprecated",
    "meth-deprecated",
    "class",
    "virtual",
]

type DataDict = dict[Category, set[str]]


class SourceDataListValue(t.NamedTuple):
    source: str
    value: str


type SourceDataDict = dict[Category, set[SourceDataListValue]]


class ResultDataListValue(t.TypedDict):
    source: str
    value: str


type ResultDataDict = dict[Category, list[ResultDataListValue]]


def extract_globals_data_from_xml_source(path: pathlib.Path) -> SourceDataDict:
    data: SourceDataDict = {
        "const": set(),
        "const-deprecated": set(),
        "enum": set(),
        "meth": set(),
        "meth-deprecated": set(),
    }

    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        logger.error(f"Failed to parse '{path}")
        return data

    for constant in root.findall("./constants/constant"):
        constant_name = constant.get("name")
        if constant_name is None:
            logger.error(f"Failed to extract constant name from '{path}")
            continue

        if constant.get("deprecated") is None:
            data["const"].add(SourceDataListValue(path.name, constant_name))
        else:
            data["const-deprecated"].add(SourceDataListValue(path.name, constant_name))

        enum_name = constant.get("enum")
        if enum_name is not None:
            data["enum"].add(SourceDataListValue(path.name, enum_name))

    for method in root.findall("./methods/method"):
        method_name = method.get("name")
        if method_name is None:
            logger.error(f"Failed to extract method name from '{path}")
            continue

        if method.get("deprecated") is None:
            data["meth"].add(SourceDataListValue(path.name, method_name))
        else:
            data["meth-deprecated"].add(SourceDataListValue(path.name, method_name))

    return data


def extract_classes_data_from_xml_source(classes_dir: pathlib.Path) -> SourceDataDict:
    data: SourceDataDict = {
        "class": set(),
        "virtual": set(),
    }

    for path in classes_dir.glob("*.xml"):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            logger.error(f"Failed to parse '{path}")
            continue

        class_name = root.get("name")
        if not class_name:
            logger.error(f"Failed to extract class name from '{path}")
            continue

        data["class"].add(SourceDataListValue(path.name, class_name))

        for method in root.findall("./methods/method"):
            if "virtual" in method.get("qualifiers", ""):
                method_name = method.get("name")
                if method_name is None:
                    logger.error(f"Failed to extract method name from '{path}")
                    continue

                data["virtual"].add(SourceDataListValue(path.name, method_name))

    return data


def extract_grammar_regexes(group_name: str) -> DataDict:
    data: DataDict = {}

    source_lines = grammar_file.read_text().splitlines()

    for cat in CATEGORIES:
        data[cat] = set()

        start_marker = f"# {group_name} - {cat} - START"
        end_marker = f"# {group_name} - {cat} - END"
        start_marker_indexes = []
        end_marker_indexes = []
        for idx, line in enumerate(source_lines):
            if start_marker in line:
                start_marker_indexes.append(idx)
            elif end_marker in line:
                end_marker_indexes.append(idx)

        if len(start_marker_indexes) != len(end_marker_indexes):
            raise AssertionError(
                f"Unequal amount of start and end marker comments: '{group_name} - {cat}'"
            )

        for i in range(len(start_marker_indexes)):
            start_idx = start_marker_indexes[i]
            end_idx = end_marker_indexes[i]
            if start_idx >= end_idx:
                raise AssertionError(
                    f"Start idx ({start_idx}) > end idx ({end_idx}): '{group_name} - {cat}'"
                )
            regex_source = source_lines[(start_idx + 1) : end_idx]
            data[cat].add(f"(?x){'\n'.join(regex_source)}")

    return data


def check_source_against_grammar_regexes(
    godot_source_data: SourceDataDict,
    grammar_regex_sources: DataDict,
) -> ResultDataDict:
    results: ResultDataDict = {}

    for cat in CATEGORIES:
        regexes = [re.compile(regex) for regex in grammar_regex_sources.get(cat, [])]

        results[cat] = [
            {"source": source_data.source, "value": source_data.value}
            for source_data in godot_source_data.get(cat, set())
            if not any(regex.search(source_data.value) for regex in regexes)
        ]

        if len(results[cat]) == 0:
            del results[cat]

    return results


def main() -> int:
    target = sys.argv[2] if len(sys.argv) >= 2 else "master"

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = pathlib.Path(temp_dir_str)

        logger.info("Clone repo")
        subprocess.check_call(
            [
                "git",
                "clone",
                "--depth=1",
                "--filter=blob:none",
                "--sparse",
                f"--branch={target}",
                "https://github.com/godotengine/godot.git",
            ],
            cwd=temp_dir,
        )
        repo_dir = temp_dir / "godot"

        godot_source_data = {}
        for source_file in GLOBALS_SOURCE_FILES:
            logger.info(f"Sparse-checkout: {source_file.parent}")
            subprocess.check_call(
                ["git", "sparse-checkout", "set", source_file.parent],
                cwd=repo_dir,
            )

            logger.info(f"Extracting data from '{source_file}'")
            godot_source_data[source_file.stem] = extract_globals_data_from_xml_source(
                repo_dir / source_file
            )

        classes_source_dir = "doc/classes"
        classes_key = "Classes"
        logger.info(f"Sparse-checkout: {classes_source_dir}")
        subprocess.check_call(
            ["git", "sparse-checkout", "set", classes_source_dir],
            cwd=repo_dir,
        )
        classes_dir = repo_dir / classes_source_dir

        logger.info(f"Extracting data from '{classes_source_dir}'")
        godot_source_data[classes_key] = extract_classes_data_from_xml_source(
            classes_dir
        )

    grammar_regex_sources = {}
    for source_file in GLOBALS_SOURCE_FILES:
        logger.info(f"Extracting grammar regexes for '{source_file.stem}'")
        grammar_regex_sources[source_file.stem] = extract_grammar_regexes(
            source_file.stem
        )

    logger.info(f"Extracting grammar regexes for '{classes_key}'")
    grammar_regex_sources[classes_key] = extract_grammar_regexes(classes_key)

    comparison_results = {}
    for source_file in GLOBALS_SOURCE_FILES:
        logger.info(f"Check missing values for '{source_file.stem}'")
        comparison_results[source_file.stem] = check_source_against_grammar_regexes(
            godot_source_data[source_file.stem],
            grammar_regex_sources[source_file.stem],
        )

    logger.info(f"Check missing values for '{classes_key}'")
    comparison_results[classes_key] = check_source_against_grammar_regexes(
        godot_source_data[classes_key],
        grammar_regex_sources[classes_key],
    )

    rv = (
        1
        if any(
            len(r.get(cat, []))
            for cat in CATEGORIES
            for r in comparison_results.values()
        )
        else 0
    )

    if rv:
        logger.error("Grammar file is missing values, see below.")
        json_str = json.dumps(comparison_results, indent=2)
        logger.error(json_str)
        (out_file).write_text(json_str)

    logger.info("Finished...")

    return rv


if __name__ == "__main__":
    sys.exit(main())
