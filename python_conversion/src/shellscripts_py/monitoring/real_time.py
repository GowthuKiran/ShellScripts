from __future__ import annotations

import argparse

from shellscripts_py.monitoring.process_status import process_running


def scan_services(service_names: list[str]) -> list[str]:
    results: list[str] = []
    for service in service_names:
        status = "Running" if process_running(service) else "Not Running"
        results.append(f"{service}: {status}")
    return results


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Check a set of services at once.")
    parser.add_argument("services", nargs="+")
    args = parser.parse_args(argv)

    for result in scan_services(args.services):
        print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
