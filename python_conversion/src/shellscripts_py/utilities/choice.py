from __future__ import annotations

import argparse


def service_action(choice: str) -> str:
    normalized = choice.strip().lower()
    mapping = {
        "start": "service started....",
        "stop": "service stopped.....",
        "status": "service is running",
    }
    return mapping.get(normalized, "Entered incorrect choice")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Choose a service action.")
    parser.add_argument("choice")
    args = parser.parse_args(argv)

    print(service_action(args.choice))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
