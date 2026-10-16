"""Starting point for an init-example command."""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="init-example",
        description="Starting point for a new initialization tool.",
    )
    return parser.parse_args()


def main() -> None:
    parse_args()
    # Replace this message with the tool's behavior.
    print("init-example: customize init_example.py to implement your tool.")


if __name__ == "__main__":
    main()
