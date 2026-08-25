#!/usr/bin/env python3
from __future__ import annotations
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <directory name>")
        return 1

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print("Given path is not a directory")
        return 1

    file_count = sum(1 for p in directory.iterdir() if p.is_file())
    if file_count > 0:
        print(f"Number of files in the given directory are: {file_count}")
    else:
        print("There are no files in the given directory")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
