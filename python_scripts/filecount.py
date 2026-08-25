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
        print("Given directory does not exist")
        return 1

    files = [p for p in directory.iterdir() if p.is_file()]
    top_files = sorted(files, key=lambda p: p.stat().st_size, reverse=True)[:5]
    for p in top_files:
        size_mb = p.stat().st_size / (1024 * 1024)
        print(f"{size_mb:.2f} MB\t{p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
