#!/usr/bin/env python3
"""Remove `//` comments from *.jsonc file and save it as *.json file."""
import re
import sys

from pathlib import Path
from typing import List

# Regex workspace: https://regex101.com/r/fllrje/9
JSON_PATTERN = re.compile(
    r"""(?x)(?# Ignore whitespace)
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
)

remove_comment = lambda json_line: JSON_PATTERN.sub(repl=r"\1", string=json_line)


def main(files: List[str]) -> int:
    """Remove comments from given *.jsonc files.

    :param files: List of files to remove comments from.
    :return: Exit code
    """
    exit_code = 0

    for file in files:
        file_path = Path(file)
        json_file_path = file_path.with_suffix(".json")

        if not file_path.is_file():
            print(f"File '{file_path}' does not exist.")
            exit_code = 1
            continue

        if file_path.suffix != ".jsonc":
            print(f"File '{file_path}' is not a '*.jsonc' file.")
            exit_code = 1
            continue

        jsonc_content = file_path.read_text().split("\n")

        json_content_wo_comments = [
            remove_comment(l) for l in jsonc_content if remove_comment(l).strip() != ""
        ]

        if not json_file_path.is_file():
            print(f"Created file '{json_file_path}'.")
            json_file_path.write_text("\n".join(json_content_wo_comments))
            exit_code = 1

        elif json_file_path.read_text().split("\n") != json_content_wo_comments:
            print(f"Updated file '{json_file_path}'.")
            json_file_path.write_text("\n".join(json_content_wo_comments))
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
