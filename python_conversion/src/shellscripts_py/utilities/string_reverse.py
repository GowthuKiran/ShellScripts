from __future__ import annotations

import argparse


def reverse_string(value: str) -> str:
    return value[::-1]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Reverse a string.")
    parser.add_argument("value")
    args = parser.parse_args(argv)

    print(f"Original String {args.value}")
    print(f"Reverse String {reverse_string(args.value)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
