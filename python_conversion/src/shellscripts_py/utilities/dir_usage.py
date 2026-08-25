from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.common import require


def directory_usage(directory: str | Path) -> int:
    target = Path(directory).expanduser()
    require(target.exists(), f"Directory does not exist: {target}")
    require(target.is_dir(), f"Not a directory: {target}")

    total = 0
    for entry in target.rglob("*"):
        if entry.is_file():
            total += entry.stat().st_size
    return total


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Summarize directory size.")
    parser.add_argument("directory")
    args = parser.parse_args(argv)

    print(f"Directory size: {directory_usage(args.directory)} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
