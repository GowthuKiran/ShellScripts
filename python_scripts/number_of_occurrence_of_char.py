#!/usr/bin/env python3
from __future__ import annotations


def main() -> int:
    char = input("Enter the character to search: ")
    if not char:
        print("Character input cannot be empty")
        return 1
    char = char[0]

    print("Choose input type:")
    print("1. From a file")
    print("2. From a string")
    choice = input().strip()

    if choice == "1":
        filename = input("Enter file name: ").strip()
        try:
            with open(filename, "r", encoding="utf-8", errors="replace") as f:
                text = f.read()
        except FileNotFoundError:
            print("File not found!")
            return 1
        print(f"The character '{char}' occurred {text.count(char)} times in file '{filename}'.")
    elif choice == "2":
        input_string = input("Enter the string: ")
        print(f"The character '{char}' occurred {input_string.count(char)} times in the given string.")
    else:
        print("Invalid choice!")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
