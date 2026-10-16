"""Starting point for an example-tool command."""

import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="example-tool",
        description="Starting point for a new Python command-line tool.",
    )
    return parser.parse_args()


def main() -> None:
    parse_args()
    # Replace this message with the tool's behavior.
    print("example-tool: customize example_tool.py to implement your tool.")


if __name__ == "__main__":
    main()
