#!/usr/bin/env python3


def main() -> int:
    text = input("Enter String to reverse: ")
    print(f"Original String {text}")
    print(f"Reverse String {text[::-1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
