from __future__ import annotations

import argparse


def loop_numbers(limit: int = 5) -> list[int]:
    return list(range(1, limit + 1))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Print numbers from 1 to N.")
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args(argv)

    for number in loop_numbers(args.limit):
        print(number)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
