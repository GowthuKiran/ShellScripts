from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.common import require


def count_character_in_text(value: str, target: str) -> int:
    require(len(target) == 1, "Target character should be a single character")
    return value.count(target)


def count_character_in_file(file_path: str | Path, target: str) -> int:
    require(len(target) == 1, "Target character should be a single character")
    source = Path(file_path).expanduser()
    require(source.exists(), f"File does not exist: {source}")
    require(source.is_file(), f"Not a file: {source}")

    with source.open("r", encoding="utf-8", errors="replace") as file_obj:
        content = file_obj.read()
    return content.count(target)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Count occurrences of a character in text or a file.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--text")
    group.add_argument("--file")
    parser.add_argument("--char", required=True)
    args = parser.parse_args(argv)

    if args.text is not None:
        print(f"The character '{args.char}' occurred {count_character_in_text(args.text, args.char)} times in the given string.")
    else:
        print(f"The character '{args.char}' occurred {count_character_in_file(args.file, args.char)} times in file '{args.file}'.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
