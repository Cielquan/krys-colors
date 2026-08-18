#!/usr/bin/env python3
"""Script to update the list of virtual methods in `gdscript.tmLanguage.yaml` grammar file."""

import logging
import pathlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)


ext_dir = pathlib.Path(__file__).parent / ".."
grammar_file = ext_dir / "syntaxes/gdscript.tmLanguage.yaml"


START_MARKER = "          # VIRTUAL_METHODS_START"
END_MARKER = "          # VIRTUAL_METHODS_END"


def extract_virtual_methods_from_xml_source(
    classes_dir: pathlib.Path,
) -> dict[str, list[str]]:
    class_methods_dict: dict[str, list[str]] = {}

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

        methods = []

        for method in root.findall("./methods/method"):
            if "virtual" in method.get("qualifiers", ""):
                method_name = method.get("name")
                if method_name is None:
                    logger.error(f"Failed to extract method name from '{path}")
                    continue
                methods.append(method_name)

        if not methods:
            continue

        if class_name in class_methods_dict:
            logger.error(f"Duplicate class_name: '{class_name}'")
            continue

        class_methods_dict[class_name] = methods

    return class_methods_dict


def generate_regex_lines(data: dict[str, list[str]]) -> list[str]:
    regex_lines: list[str] = []

    is_first_method = True
    for class_name in sorted(data):
        regex_lines.append(f"          (?# {class_name})")
        for method in sorted(data[class_name]):
            if is_first_method:
                regex_lines.append(f"          {method.removeprefix('_')}")
                is_first_method = False
                continue
            regex_lines.append(f"          |{method.removeprefix('_')}")

    return regex_lines


def main() -> int:
    target = sys.argv[2] if len(sys.argv) >= 2 else "master"

    with tempfile.TemporaryDirectory() as temp_dir_str:
        temp_dir = pathlib.Path(temp_dir_str)

        print("## Clone repo")
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

        print("## Sparse-checkout")
        subprocess.check_call(
            ["git", "sparse-checkout", "set", "doc/classes"],
            cwd=repo_dir,
        )
        classes_dir = repo_dir / "doc" / "classes"

        methods_dict = extract_virtual_methods_from_xml_source(classes_dir)
        regex_lines = generate_regex_lines(methods_dict)

        grammar_lines = grammar_file.read_text().splitlines()
        start_idx = grammar_lines.index(START_MARKER)
        end_idx = grammar_lines.index(END_MARKER)

        new_grammar_lines = (
            grammar_lines[: (start_idx + 1)]
            + regex_lines
            + grammar_lines[(end_idx - 1) :]
        )

        grammar_file.write_text("\n".join(new_grammar_lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
