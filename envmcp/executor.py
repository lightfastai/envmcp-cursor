"""
Command execution functionality for envmcp.
"""

import os
import subprocess
import sys
from typing import List, Optional


def execute_command(command: str, args: Optional[List[str]] = None) -> None:
    """
    Executes a command with the given arguments using the current environment.

    Args:
        command: The command to execute.
        args: The arguments for the command. Defaults to empty list.
    """
    if args is None:
        args = []

    # Combine command and args for subprocess
    cmd_list = [command, *args]

    try:
        # Execute the command with current environment
        # Using subprocess.run with shell=False for better security
        # but we need to handle shell commands properly

        # Check if this looks like a shell command that needs shell=True
        needs_shell = any(
            char in command for char in ["|", "&", ";", ">", "<", "`", "$"]
        )

        if needs_shell:
            # For shell commands, join everything into a single string
            cmd_str = " ".join([command, *args])
            process = subprocess.run(cmd_str, shell=True, env=os.environ.copy())
        else:
            # For regular commands, use the safer approach
            process = subprocess.run(cmd_list, env=os.environ.copy())

        # Exit with the same code as the child process
        sys.exit(process.returncode)

    except FileNotFoundError:
        print(f"Error: Command not found: {command}", file=sys.stderr)
        sys.exit(127)  # Command not found exit code
    except PermissionError:
        print(f"Error: Permission denied executing: {command}", file=sys.stderr)
        sys.exit(126)  # Permission denied exit code
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)  # Interrupted by Ctrl+C
    except Exception as error:
        print(f"Error executing command: {error}", file=sys.stderr)
        sys.exit(1)
