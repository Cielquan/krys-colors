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
out_file = ext_dir / "missing-globals.bak.json"


SOURCE_FILES = (
    pathlib.Path("modules/gdscript/doc_classes/@GDScript.xml"),
    pathlib.Path("doc/classes/@GlobalScope.xml"),
)

type Category = t.Literal[
    "const",
    "meth",
    "enum",
    "const-deprecated",
    "meth-deprecated",
]
CATEGORIES: list[Category] = [
    "const",
    "meth",
    "enum",
    "const-deprecated",
    "meth-deprecated",
]

type DataDict = dict[Category, list[str]]


def extract_data_from_globals_xml_source(
    path: pathlib.Path,
) -> DataDict:
    data: DataDict = {}
    for cat in CATEGORIES:
        data[cat] = []

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
            data["const"].append(constant_name)
        else:
            data["const-deprecated"].append(constant_name)

        enum_name = constant.get("enum")
        if enum_name is not None:
            data["enum"].append(enum_name)

    for method in root.findall("./methods/method"):
        method_name = method.get("name")
        if method_name is None:
            logger.error(f"Failed to extract method name from '{path}")
            continue

        if method.get("deprecated") is None:
            data["meth"].append(method_name)
        else:
            data["meth-deprecated"].append(method_name)

    data["const"] = sorted(set(data["const"]))
    data["const-deprecated"] = sorted(set(data["const-deprecated"]))
    data["enum"] = sorted(set(data["enum"]))
    data["meth"] = sorted(set(data["meth"]))

    return data


def extract_grammar_regexes_for_globals(
    file_stem: str,
) -> DataDict:
    data: DataDict = {}

    source_lines = grammar_file.read_text().splitlines()

    for cat in CATEGORIES:
        data[cat] = []

        start_marker = f"# {file_stem} - {cat} - START"
        end_marker = f"# {file_stem} - {cat} - END"
        start_marker_indexes = []
        end_marker_indexes = []
        for idx, line in enumerate(source_lines):
            if start_marker in line:
                start_marker_indexes.append(idx)
            elif end_marker in line:
                end_marker_indexes.append(idx)

        if len(start_marker_indexes) != len(end_marker_indexes):
            raise AssertionError(
                f"Unequal amount of start and end marker comments: '{file_stem} - {cat}'"
            )

        for i in range(len(start_marker_indexes)):
            start_idx = start_marker_indexes[i]
            end_idx = end_marker_indexes[i]
            if start_idx >= end_idx:
                raise AssertionError(
                    f"Start idx ({start_idx}) > end idx ({end_idx}): '{file_stem} - {cat}'"
                )
            regex_source = source_lines[(start_idx + 1) : end_idx]
            data[cat].append(f"(?x){'\n'.join(regex_source)}")

    return data


def check_globals_source_against_grammar_regexes(
    godot_source_data: DataDict,
    grammar_regex_sources: DataDict,
) -> DataDict:
    results: DataDict = {}

    for cat in CATEGORIES:
        regexes = [re.compile(regex) for regex in grammar_regex_sources[cat]]

        results[cat] = [
            source_name
            for source_name in godot_source_data[cat]
            if not any(regex.search(source_name) for regex in regexes)
        ]

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

        godot_globals_source_data = {}
        for source_file in SOURCE_FILES:
            logger.info(f"Sparse-checkout: {source_file.parent}")
            subprocess.check_call(
                ["git", "sparse-checkout", "set", source_file.parent],
                cwd=repo_dir,
            )

            logger.info(f"Extracting data from '{source_file}'")
            godot_globals_source_data[source_file.name] = (
                extract_data_from_globals_xml_source(repo_dir / source_file)
            )

        globals_grammar_regex_sources = {}
        for source_file in SOURCE_FILES:
            logger.info(f"Extracting grammar regexes for '{source_file.stem}'")
            globals_grammar_regex_sources[source_file.name] = (
                extract_grammar_regexes_for_globals(source_file.stem)
            )

        globals_comparison_results = {}
        for source_file in SOURCE_FILES:
            logger.info(f"Check missing values for '{source_file.stem}'")
            globals_comparison_results[source_file.name] = (
                check_globals_source_against_grammar_regexes(
                    godot_globals_source_data[source_file.name],
                    globals_grammar_regex_sources[source_file.name],
                )
            )

    rv = (
        1
        if any(
            len(r[cat])
            for cat in CATEGORIES
            for r in globals_comparison_results.values()
        )
        else 0
    )

    if rv:
        logger.error("Grammar file is missing values, see below.")
        json_str = json.dumps(globals_comparison_results, indent=2)
        logger.error(json_str)
        (out_file).write_text(json_str)

    logger.info("Finished...")

    return rv


if __name__ == "__main__":
    sys.exit(main())
