#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
import time
from pathlib import Path


def follow(path: Path):
    with path.open("r", encoding="utf-8", errors="replace") as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.2)
                continue
            yield line.rstrip("\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Monitor a log file and print alerts for patterns")
    parser.add_argument("log_file", type=Path)
    parser.add_argument("--patterns", nargs="+", default=["ERROR", "WARN", "INFO"])
    args = parser.parse_args()

    if not args.log_file.exists():
        print(f"Log file not found: {args.log_file}")
        return 1

    compiled = [re.compile(p) for p in args.patterns]
    for line in follow(args.log_file):
        for pattern in compiled:
            if pattern.search(line):
                print(f"ALERT: Pattern {pattern.pattern} found in log: {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
