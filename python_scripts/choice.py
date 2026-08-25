#!/usr/bin/env python3

def main() -> int:
    choice = input("Enter your choice (start/stop/status): ").strip().lower()
    if choice == "start":
        print("service started....")
    elif choice == "stop":
        print("service stopped.....")
    elif choice == "status":
        print("service is running")
    else:
        print("Entered incorrect choice")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
