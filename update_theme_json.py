#!/usr/bin/env python3
"""Remove `//` comments from *.jsonc file and save it as *.json file."""
import re
import sys

from pathlib import Path
from typing import List

# Regex workspace: https://regex101.com/r/fllrje/9
PATTERN = r"""
(?x)(?# Ignore whitespace)
(?# Start capturing group at beginning...)
^(
(?# ...with optional whitespace except newlines)
[^\S\r\n]*
    (?:(?# Find a double quoted string...)
        (?:\"
            (?:(?# ...containing escapted quotes `\"` or chars != `"`)
                (?:\\\")|[^\"]
            )*
        \")
    |(?# ...OR chars except `"` or `/` e.g. whitespace `null` `:` `[]`)
        [^\"/]*?
    )*
)(?# End capturing group)
(?# Optinally match whitespace except newlines and `//` comment before EOL)
(?:[^\S\r\n]*//.*)?$
"""


def remove_comment(line: str) -> str:
    """Remove JS style comments from given string.

    :param line: Line to check
    :return: Line without comment
    """
    return re.sub(pattern=PATTERN, repl=r"\1", string=line)


def main(files: List[str]) -> int:
    """Remove comments from given files.

    :param files: List of files to remove comments from.
    :return: Exit code
    """
    exit_code = 0
    for file in files:
        file_path = Path(file)

        if not file_path.is_file():
            print(f"File '{file_path}' does not exist.")
            exit_code = 1
            continue

        jsonc_content = file_path.read_text().split("\n")

        if file_path.suffix == ".jsonc":
            file_path = file_path.with_suffix(".json")

        json_content = [
            remove_comment(l) for l in jsonc_content if remove_comment(l).strip() != ""
        ]

        file_path.write_text("\n".join(json_content))
        print(f"Created/Updated file '{file_path}'.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
