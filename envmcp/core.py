"""
Core functionality for envmcp - environment file discovery, parsing, and loading.
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional


def find_env_file(start_dir: Optional[str] = None) -> Optional[str]:
    """
    Finds the closest .env.mcp file by traversing up the directory tree.

    Args:
        start_dir: The directory to start searching from. Defaults to current
            working directory.

    Returns:
        The path to the found .env.mcp file or None if not found.
    """
    if start_dir is None:
        start_dir = os.getcwd()

    current_dir = Path(start_dir).resolve()

    # Continue checking until we reach the root directory
    while True:
        env_file_path = current_dir / ".env.mcp"

        try:
            if env_file_path.exists() and env_file_path.is_file():
                return str(env_file_path)
        except (OSError, PermissionError) as err:
            print(f"Error checking file at {env_file_path}: {err}", file=sys.stderr)

        # Move up to the parent directory
        parent_dir = current_dir.parent

        # Stop if we've reached the root directory
        if parent_dir == current_dir:
            break

        current_dir = parent_dir

    # Special case: Check for ~/.env.mcp
    home_dir = Path.home()
    home_env_file = home_dir / ".env.mcp"

    try:
        if home_env_file.exists() and home_env_file.is_file():
            return str(home_env_file)
    except (OSError, PermissionError) as err:
        print(f"Error checking file at {home_env_file}: {err}", file=sys.stderr)

    return None


def parse_env_file(file_path: str) -> Dict[str, str]:
    """
    Parses an environment file and returns its contents as key-value pairs.

    Args:
        file_path: Path to the environment file.

    Returns:
        Dictionary containing environment variables.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        PermissionError: If the file can't be read.
    """
    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError as err:
        raise FileNotFoundError(f"Environment file not found: {file_path}") from err
    except PermissionError as err:
        raise PermissionError(f"Permission denied reading file: {file_path}") from err

    result: Dict[str, str] = {}

    # Split by newlines and process each line
    lines = content.splitlines()

    for line_num, line in enumerate(lines, 1):
        # Skip empty lines and comments
        trimmed_line = line.strip()
        if not trimmed_line or trimmed_line.startswith("#"):
            continue

        # Parse key=value format
        if "=" not in trimmed_line:
            print(
                f"Warning: Invalid line format at line {line_num}: {line}",
                file=sys.stderr,
            )
            continue

        key, _, value = trimmed_line.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            print(f"Warning: Empty key at line {line_num}: {line}", file=sys.stderr)
            continue

        # Remove surrounding quotes if present
        if len(value) >= 2:
            if (value.startswith('"') and value.endswith('"')) or (
                value.startswith("'") and value.endswith("'")
            ):
                value = value[1:-1]

        result[key] = value

    return result


def load_env_mcp(custom_path: Optional[str] = None) -> bool:
    """
    Loads environment variables from a .env.mcp file.

    Args:
        custom_path: Optional custom path to the env file.

    Returns:
        True if environment variables were loaded successfully, False otherwise.
    """
    env_path = custom_path or find_env_file()

    if not env_path:
        print("Error: No .env.mcp file found", file=sys.stderr)
        return False

    try:
        env_vars = parse_env_file(env_path)

        # Add variables to os.environ
        for key, value in env_vars.items():
            os.environ[key] = value

        return True
    except (FileNotFoundError, PermissionError) as error:
        print(f"Error loading .env.mcp file: {error}", file=sys.stderr)
        return False
    except Exception as error:
        print(f"Unexpected error loading .env.mcp file: {error}", file=sys.stderr)
        return False
