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

    file_with_size = [(p, p.stat().st_size) for p in directory.iterdir() if p.is_file()]
    top_files = sorted(file_with_size, key=lambda item: item[1], reverse=True)[:5]
    for path, size in top_files:
        size_mb = size / (1024 * 1024)
        print(f"{size_mb:.2f} MB\t{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
