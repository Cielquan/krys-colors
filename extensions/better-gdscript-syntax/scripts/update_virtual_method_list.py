#!/usr/bin/env python3
"""Script to update the list of virtual methods in `gdscript.tmLanguage.yaml` grammar file."""

import logging
import pathlib
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

ext_dir = pathlib.Path(__file__).parent / ".."
grammar_file = ext_dir / "syntaxes/gdscript.tmLanguage.yaml"


START_MARKER = "          # VIRTUAL_METHODS_START"
END_MARKER = "          # VIRTUAL_METHODS_END"


def extract_virtual_methods_from_xml_source(
    classes_dir: pathlib.Path,
) -> tuple[dict[str, set[str]], int]:
    methods_class_dict: dict[str, set[str]] = {}

    longest_name = 0

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

        for method in root.findall("./methods/method"):
            if "virtual" in method.get("qualifiers", ""):
                method_name = method.get("name")
                if method_name is None:
                    logger.error(f"Failed to extract method name from '{path}")
                    continue
                if method_name not in methods_class_dict:
                    methods_class_dict[method_name] = set()
                methods_class_dict[method_name].add(class_name)
                longest_name = max(longest_name, len(method_name))

    return methods_class_dict, longest_name


def generate_regex_lines(data: dict[str, set[str]], longest_name: int) -> list[str]:
    regex_lines: list[str] = []

    is_first_method = True
    for method in sorted(data):
        class_names = sorted(data[method])
        padding = longest_name + 2 - len(method)
        pipe_prefix = "|"

        if is_first_method:
            padding += 1
            pipe_prefix = ""
            is_first_method = False

        regex_lines.append(
            f"          {pipe_prefix}{method.removeprefix('_')}{padding * ' '}(?# {' / '.join(class_names)})"
        )

    return regex_lines


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

        logger.info("Sparse-checkout")
        subprocess.check_call(
            ["git", "sparse-checkout", "set", "doc/classes"],
            cwd=repo_dir,
        )
        classes_dir = repo_dir / "doc" / "classes"

        logger.info("Extracting virtual methods from XML")
        methods_dict, longest_name = extract_virtual_methods_from_xml_source(
            classes_dir
        )
        regex_lines = generate_regex_lines(methods_dict, longest_name)

        logger.info("Update regex source")
        grammar_lines = grammar_file.read_text().splitlines()
        start_idx = grammar_lines.index(START_MARKER)
        end_idx = grammar_lines.index(END_MARKER)

        new_grammar_lines = (
            grammar_lines[: (start_idx + 1)] + regex_lines + grammar_lines[end_idx:]
        )

        logger.info("Update grammar file")
        grammar_file.write_text("\n".join(new_grammar_lines))
        logger.info("Finished...")

        pathlib.Path("foo.txt").write_text("\n".join(regex_lines))

    return 0


if __name__ == "__main__":
    sys.exit(main())
