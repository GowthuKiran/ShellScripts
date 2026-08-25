#!/usr/bin/env python3
from __future__ import annotations
import argparse
import shutil
from datetime import datetime
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a timestamped backup copy of a file.")
    parser.add_argument("filename", type=Path)
    parser.add_argument("--backup-dir", type=Path, default=Path.cwd() / "backup")
    args = parser.parse_args()

    source = args.filename
    if not source.is_file():
        print("file doesn't exist")
        return 1

    backup_dir = args.backup_dir
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"{source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(source, backup_file)
    print("Backup of given file is completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
