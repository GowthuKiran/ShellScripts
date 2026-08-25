#!/usr/bin/env python3
from __future__ import annotations
import argparse
import subprocess


def main() -> int:
    parser = argparse.ArgumentParser(description="Check if a process is running")
    parser.add_argument("process_name")
    args = parser.parse_args()

    result = subprocess.run(["pgrep", "-x", args.process_name], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        print(f"Process '{args.process_name}' is running")
    else:
        print(f"Process '{args.process_name}' is not running")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
