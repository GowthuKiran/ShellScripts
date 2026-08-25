from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.common import require


def count_files(directory: str | Path) -> int:
    target = Path(directory).expanduser()
    require(target.exists(), f"Directory does not exist: {target}")
    require(target.is_dir(), f"Not a directory: {target}")
    return sum(1 for entry in target.iterdir() if entry.is_file())


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Count files in a directory.")
    parser.add_argument("directory")
    args = parser.parse_args(argv)

    print(f"Number of files in the given directory are: {count_files(args.directory)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
