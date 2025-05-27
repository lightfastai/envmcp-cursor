"""
Tests for envmcp.cli module.
"""

import unittest
from unittest.mock import patch, MagicMock

from envmcp.cli import parse_args, main


class TestParseArgs(unittest.TestCase):
    """Tests for parse_args function."""

    def test_parse_basic_command(self):
        """Test parsing basic command without options."""
        args = parse_args(["python", "script.py"])

        self.assertEqual(args.command, "python")
        self.assertEqual(args.args, ["script.py"])
        self.assertIsNone(args.env_file)

    def test_parse_command_with_env_file_long(self):
        """Test parsing command with --env-file option."""
        args = parse_args(["--env-file", "/path/to/.env", "python", "script.py"])

        self.assertEqual(args.command, "python")
        self.assertEqual(args.args, ["script.py"])
        self.assertEqual(args.env_file, "/path/to/.env")

    def test_parse_command_with_env_file_short(self):
        """Test parsing command with -e option."""
        args = parse_args(["-e", "/path/to/.env", "python", "script.py"])

        self.assertEqual(args.command, "python")
        self.assertEqual(args.args, ["script.py"])
        self.assertEqual(args.env_file, "/path/to/.env")

    def test_parse_command_with_multiple_args(self):
        """Test parsing command with multiple arguments."""
        args = parse_args(["python", "script.py", "arg1", "arg2"])

        self.assertEqual(args.command, "python")
        self.assertEqual(args.args, ["script.py", "arg1", "arg2"])
        self.assertIsNone(args.env_file)

    def test_parse_no_command_raises_error(self):
        """Test that missing command raises SystemExit."""
        with self.assertRaises(SystemExit):
            parse_args([])

    def test_parse_env_file_without_path_raises_error(self):
        """Test that --env-file without path raises SystemExit."""
        with self.assertRaises(SystemExit):
            parse_args(["--env-file"])

    def test_parse_version_flag(self):
        """Test that --version flag raises SystemExit."""
        with self.assertRaises(SystemExit):
            parse_args(["--version"])

    def test_parse_help_flag(self):
        """Test that --help flag raises SystemExit."""
        with self.assertRaises(SystemExit):
            parse_args(["--help"])


class TestMain(unittest.TestCase):
    """Tests for main function."""

    @patch("envmcp.cli.execute_command")
    @patch("envmcp.cli.load_env_mcp")
    @patch("envmcp.cli.parse_args")
    def test_main_success(
        self, mock_parse_args, mock_load_env_mcp, mock_execute_command
    ):
        """Test successful main execution."""
        # Mock parsed arguments
        mock_args = MagicMock()
        mock_args.command = "python"
        mock_args.args = ["script.py"]
        mock_args.env_file = None
        mock_parse_args.return_value = mock_args

        # Mock successful env loading
        mock_load_env_mcp.return_value = True

        # Call main
        main()

        # Verify calls
        mock_parse_args.assert_called_once()
        mock_load_env_mcp.assert_called_once_with(None)
        mock_execute_command.assert_called_once_with("python", ["script.py"])

    @patch("envmcp.cli.execute_command")
    @patch("envmcp.cli.load_env_mcp")
    @patch("envmcp.cli.parse_args")
    def test_main_with_custom_env_file(
        self, mock_parse_args, mock_load_env_mcp, mock_execute_command
    ):
        """Test main execution with custom env file."""
        # Mock parsed arguments
        mock_args = MagicMock()
        mock_args.command = "python"
        mock_args.args = ["script.py"]
        mock_args.env_file = "/custom/.env"
        mock_parse_args.return_value = mock_args

        # Mock successful env loading
        mock_load_env_mcp.return_value = True

        # Call main
        main()

        # Verify calls
        mock_parse_args.assert_called_once()
        mock_load_env_mcp.assert_called_once_with("/custom/.env")
        mock_execute_command.assert_called_once_with("python", ["script.py"])

    @patch("envmcp.cli.load_env_mcp")
    @patch("envmcp.cli.parse_args")
    def test_main_env_load_failure(self, mock_parse_args, mock_load_env_mcp):
        """Test main execution when env loading fails."""
        # Mock parsed arguments
        mock_args = MagicMock()
        mock_args.env_file = None
        mock_parse_args.return_value = mock_args

        # Mock failed env loading
        mock_load_env_mcp.return_value = False

        # Call main and expect SystemExit
        with self.assertRaises(SystemExit) as cm:
            main()

        # Verify exit code
        self.assertEqual(cm.exception.code, 1)

        # Verify calls
        mock_parse_args.assert_called_once()
        mock_load_env_mcp.assert_called_once_with(None)

    @patch("envmcp.cli.parse_args")
    def test_main_parse_args_failure(self, mock_parse_args):
        """Test main execution when argument parsing fails."""
        # Mock parse_args raising SystemExit
        mock_parse_args.side_effect = SystemExit(2)

        # Call main and expect SystemExit
        with self.assertRaises(SystemExit) as cm:
            main()

        # Verify exit code
        self.assertEqual(cm.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
