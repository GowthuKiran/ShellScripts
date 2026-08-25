#!/usr/bin/env python3
import sys
from pathlib import Path
import shutil


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {Path(sys.argv[0]).name} <directory name>")
        return 1

    directory = Path(sys.argv[1])
    if not directory.is_dir():
        print("Given path is not a directory")
        return 1

    usage = shutil.disk_usage(directory)
    total_gb = usage.total / (1024 ** 3)
    used_gb = usage.used / (1024 ** 3)
    free_gb = usage.free / (1024 ** 3)
    print(f"Disk usage for {directory}:")
    print(f"Total: {total_gb:.2f} GB")
    print(f"Used : {used_gb:.2f} GB")
    print(f"Free : {free_gb:.2f} GB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
