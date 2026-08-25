from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.common import require


def find_matches(lines: list[str] | tuple[str, ...], patterns: list[str]) -> list[str]:
    normalized = [pattern.strip() for pattern in patterns if pattern and pattern.strip()]
    if not normalized:
        normalized = ["ERROR", "WARN", "INFO"]

    matches = []
    for line in lines:
        for pattern in normalized:
            if pattern.lower() in line.lower():
                matches.append(f"Pattern {pattern} found in log: {line.rstrip()}")
                break
    return matches


def monitor_log_file(log_file: str | Path, patterns: list[str] | None = None) -> list[str]:
    path = Path(log_file).expanduser()
    require(path.exists(), f"Log file does not exist: {path}")
    require(path.is_file(), f"Not a file: {path}")

    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    matches = find_matches(lines, patterns or ["ERROR", "WARN", "INFO"])
    for entry in matches:
        print(entry)
    return matches


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Monitor a log file for matching patterns.")
    parser.add_argument("log_file")
    parser.add_argument("--pattern", action="append", default=[])
    args = parser.parse_args(argv)

    monitor_log_file(args.log_file, args.pattern)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
