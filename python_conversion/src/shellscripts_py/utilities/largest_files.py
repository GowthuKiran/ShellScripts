from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.common import require


def largest_files(directory: str | Path, limit: int = 5) -> list[tuple[str, int]]:
    target = Path(directory).expanduser()
    require(target.exists(), f"Directory does not exist: {target}")
    require(target.is_dir(), f"Not a directory: {target}")

    results = []
    for entry in target.iterdir():
        if entry.is_file():
            results.append((str(entry), entry.stat().st_size))
    results.sort(key=lambda item: item[1], reverse=True)
    return results[:limit]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Show the largest files in a directory.")
    parser.add_argument("directory")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)

    for file_name, size in largest_files(args.directory, args.limit):
        print(f"{file_name}: {size} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
