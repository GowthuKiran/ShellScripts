from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from shellscripts_py.common import require, timestamped_backup_path


def backup_file(file_path: str | Path, backup_dir: str | Path = "backup") -> Path:
    source = Path(file_path).expanduser()
    require(source.exists(), f"File does not exist: {source}")
    require(source.is_file(), f"Not a file: {source}")

    destination = timestamped_backup_path(source, backup_dir)
    shutil.copy2(source, destination)
    return destination


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Create a timestamped backup of a file.")
    parser.add_argument("file_path")
    parser.add_argument("--backup-dir", default="backup")
    args = parser.parse_args(argv)

    destination = backup_file(args.file_path, args.backup_dir)
    print(f"Backup of given file is completed successfully: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
