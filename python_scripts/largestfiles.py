#!/usr/bin/env python3
import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <directory name>")
        return 1

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print("Given directory does not exist")
        return 1

    # Match original shell behavior: scan only top-level files in the given directory.
    file_with_size = []
    for path in directory.iterdir():
        if not path.is_file():
            continue
        try:
            file_with_size.append((path, path.stat().st_size))
        except PermissionError:
            continue
    top_files = sorted(file_with_size, key=lambda item: item[1], reverse=True)[:5]
    for path, size in top_files:
        size_mb = size / (1024 * 1024)
        print(f"{size_mb:.2f} MB\t{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
