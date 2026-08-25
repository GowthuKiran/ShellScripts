from __future__ import annotations

import argparse
import shutil
import subprocess

from shellscripts_py.common import require


def process_running(process_name: str) -> bool:
    require(bool(process_name and process_name.strip()), "Process name must not be empty")
    if shutil.which("pgrep") is None:
        return False
    completed = subprocess.run(["pgrep", "-x", process_name], capture_output=True, text=True, check=False)
    return completed.returncode == 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check whether a process is running.")
    parser.add_argument("process_name")
    args = parser.parse_args(argv)

    print("Process is running" if process_running(args.process_name) else "Process is not running")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
