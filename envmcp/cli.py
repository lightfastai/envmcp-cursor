#!/usr/bin/env python3
"""
Command-line interface for envmcp.
"""

import argparse
import sys
from typing import List, Optional

from .core import load_env_mcp
from .executor import execute_command


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """
    Parse command line arguments.

    Args:
        args: List of arguments to parse. If None, uses sys.argv.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        prog="envmcp",
        description="A lightweight way to use environment variables in your "
        "Cursor MCP server definitions.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  envmcp python script.py $API_KEY
  envmcp --env-file /path/to/.env.mcp uvicorn app:app --host $HOST
  envmcp -e custom.env pytest --env $TEST_ENV
        """,
    )

    parser.add_argument(
        "--env-file",
        "-e",
        dest="env_file",
        metavar="PATH",
        help="Specify a custom path to the environment file",
    )

    parser.add_argument("command", help="The command to execute")

    parser.add_argument(
        "args", nargs=argparse.REMAINDER, help="Arguments to pass to the command"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 0.1.0")

    return parser.parse_args(args)


def main() -> None:
    """
    Main entry point for the CLI.
    """
    try:
        parsed_args = parse_args()
    except SystemExit as e:
        # argparse calls sys.exit() for --help, --version, or parse errors
        sys.exit(e.code)

    # Load environment variables from .env.mcp file
    if not load_env_mcp(parsed_args.env_file):
        sys.exit(1)

    # Execute the command with args
    execute_command(parsed_args.command, parsed_args.args)


if __name__ == "__main__":
    main()
