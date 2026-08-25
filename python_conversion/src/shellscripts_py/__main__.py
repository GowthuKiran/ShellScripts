from __future__ import annotations

import argparse
from pathlib import Path

from shellscripts_py.infra.tomcat_install import install_tomcat
from shellscripts_py.infra.zookeeper_install import install_zookeeper
from shellscripts_py.monitoring.log_monitoring import find_matches, monitor_log_file
from shellscripts_py.monitoring.process_status import process_running
from shellscripts_py.monitoring.real_time import scan_services
from shellscripts_py.utilities.backup import backup_file
from shellscripts_py.utilities.character_count import count_character_in_file, count_character_in_text
from shellscripts_py.utilities.choice import service_action
from shellscripts_py.utilities.dir_usage import directory_usage
from shellscripts_py.utilities.file_count import count_files
from shellscripts_py.utilities.largest_files import largest_files
from shellscripts_py.utilities.looping import loop_numbers
from shellscripts_py.utilities.string_reverse import reverse_string


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Converted Python equivalents for the shell script utilities.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    backup_parser = subparsers.add_parser("backup", help="Create a timestamped backup of a file")
    backup_parser.add_argument("file_path")
    backup_parser.add_argument("--backup-dir", default="backup")

    file_count_parser = subparsers.add_parser("file-count", help="Count files in a directory")
    file_count_parser.add_argument("directory")

    largest_parser = subparsers.add_parser("largest-files", help="List the largest files in a directory")
    largest_parser.add_argument("directory")
    largest_parser.add_argument("--limit", type=int, default=5)

    dir_usage_parser = subparsers.add_parser("dir-usage", help="Summarize directory size")
    dir_usage_parser.add_argument("directory")

    choice_parser = subparsers.add_parser("choice", help="Evaluate a service action choice")
    choice_parser.add_argument("choice")

    loop_parser = subparsers.add_parser("looping", help="Print numbers in a loop")
    loop_parser.add_argument("--limit", type=int, default=5)

    reverse_parser = subparsers.add_parser("string-reverse", help="Reverse a string")
    reverse_parser.add_argument("value")

    char_parser = subparsers.add_parser("char-count", help="Count a character in text or a file")
    char_group = char_parser.add_mutually_exclusive_group(required=True)
    char_group.add_argument("--text")
    char_group.add_argument("--file")
    char_parser.add_argument("--char", required=True)

    process_parser = subparsers.add_parser("process-status", help="Check whether a process is running")
    process_parser.add_argument("process_name")

    log_parser = subparsers.add_parser("log-monitor", help="Print alerts when patterns are found in a log file")
    log_parser.add_argument("path")
    log_parser.add_argument("--pattern", action="append", default=[])

    realtime_parser = subparsers.add_parser("real-time", help="Check several services in one pass")
    realtime_parser.add_argument("services", nargs="+")

    tomcat_parser = subparsers.add_parser("tomcat-install", help="Prepare or execute a Tomcat install plan")
    tomcat_parser.add_argument("--version", default="9.0.89")
    tomcat_parser.add_argument("--install-dir", default="/opt/tomcat")
    tomcat_parser.add_argument("--dry-run", action="store_true")

    zookeeper_parser = subparsers.add_parser("zookeeper-install", help="Prepare or execute a ZooKeeper install plan")
    zookeeper_parser.add_argument("--version", default="3.8.4")
    zookeeper_parser.add_argument("--install-dir", default="/opt/zookeeper")
    zookeeper_parser.add_argument("--data-dir", default="/var/lib/zookeeper")
    zookeeper_parser.add_argument("--dry-run", action="store_true")

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "backup":
        destination = backup_file(args.file_path, args.backup_dir)
        print(f"Backup created at: {destination}")
        return 0
    if args.command == "file-count":
        print(count_files(Path(args.directory)))
        return 0
    if args.command == "largest-files":
        for file_path, size in largest_files(Path(args.directory), limit=args.limit):
            print(f"{file_path}: {size} bytes")
        return 0
    if args.command == "dir-usage":
        print(directory_usage(Path(args.directory)))
        return 0
    if args.command == "choice":
        print(service_action(args.choice))
        return 0
    if args.command == "looping":
        for number in loop_numbers(args.limit):
            print(number)
        return 0
    if args.command == "string-reverse":
        print(reverse_string(args.value))
        return 0
    if args.command == "char-count":
        if args.text is not None:
            print(count_character_in_text(args.text, args.char))
        else:
            print(count_character_in_file(Path(args.file), args.char))
        return 0
    if args.command == "process-status":
        print("Running" if process_running(args.process_name) else "Not Running")
        return 0
    if args.command == "log-monitor":
        patterns = args.pattern or ["ERROR", "WARN", "INFO"]
        monitor_log_file(Path(args.path), patterns)
        return 0
    if args.command == "real-time":
        for result in scan_services(args.services):
            print(result)
        return 0
    if args.command == "tomcat-install":
        plan = install_tomcat(version=args.version, install_dir=args.install_dir, dry_run=args.dry_run)
        print(plan)
        return 0
    if args.command == "zookeeper-install":
        plan = install_zookeeper(version=args.version, install_dir=args.install_dir, data_dir=args.data_dir, dry_run=args.dry_run)
        print(plan)
        return 0

    parser.error(f"Unsupported command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
