#!/usr/bin/env python3
from __future__ import annotations
import shutil
import sys
from datetime import datetime
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <filename>")
        return 1

    source = Path(sys.argv[1])
    if not source.is_file():
        print("file doesn't exist")
        return 1

    backup_dir = Path("backup")
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"{source.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(source, backup_file)
    print("Backup of given file is completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
