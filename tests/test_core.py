"""
Tests for envmcp.core module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from envmcp.core import find_env_file, load_env_mcp, parse_env_file


class TestFindEnvFile(unittest.TestCase):
    """Tests for find_env_file function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self):
        """Clean up test fixtures."""
        os.chdir(self.original_cwd)
        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_find_env_file_in_current_directory(self):
        """Test finding .env.mcp in current directory."""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text("TEST=value")

        os.chdir(self.temp_dir)
        result = find_env_file()

        self.assertEqual(result, str(env_file.resolve()))

    def test_find_env_file_in_parent_directory(self):
        """Test finding .env.mcp in parent directory."""
        # Create nested directory structure
        parent_dir = Path(self.temp_dir)
        child_dir = parent_dir / "child"
        child_dir.mkdir()

        # Create .env.mcp in parent
        env_file = parent_dir / ".env.mcp"
        env_file.write_text("TEST=value")

        # Search from child directory
        result = find_env_file(str(child_dir))

        self.assertEqual(result, str(env_file.resolve()))

    def test_find_env_file_not_found(self):
        """Test when no .env.mcp file is found."""
        # Use a temporary directory with no .env.mcp file
        result = find_env_file(self.temp_dir)

        # Should return None when no file is found
        self.assertIsNone(result)

    @patch("envmcp.core.Path.home")
    def test_find_env_file_in_home_directory(self, mock_home):
        """Test finding .env.mcp in home directory as fallback."""
        # Mock home directory
        mock_home.return_value = Path(self.temp_dir)

        # Create .env.mcp in mock home directory
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text("TEST=value")

        # Search from a different directory
        search_dir = Path(self.temp_dir) / "other"
        search_dir.mkdir()

        result = find_env_file(str(search_dir))

        self.assertEqual(result, str(env_file.resolve()))


class TestParseEnvFile(unittest.TestCase):
    """Tests for parse_env_file function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_parse_simple_env_file(self):
        """Test parsing a simple environment file."""
        env_content = """
KEY1=value1
KEY2=value2
"""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text(env_content.strip())

        result = parse_env_file(str(env_file))

        expected = {"KEY1": "value1", "KEY2": "value2"}
        self.assertEqual(result, expected)

    def test_parse_env_file_with_quotes(self):
        """Test parsing environment file with quoted values."""
        env_content = """
KEY1="quoted value"
KEY2='single quoted'
KEY3=unquoted
"""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text(env_content.strip())

        result = parse_env_file(str(env_file))

        expected = {"KEY1": "quoted value", "KEY2": "single quoted", "KEY3": "unquoted"}
        self.assertEqual(result, expected)

    def test_parse_env_file_with_comments(self):
        """Test parsing environment file with comments."""
        env_content = """
# This is a comment
KEY1=value1
# Another comment
KEY2=value2
"""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text(env_content.strip())

        result = parse_env_file(str(env_file))

        expected = {"KEY1": "value1", "KEY2": "value2"}
        self.assertEqual(result, expected)

    def test_parse_env_file_with_empty_lines(self):
        """Test parsing environment file with empty lines."""
        env_content = """
KEY1=value1

KEY2=value2

"""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text(env_content)

        result = parse_env_file(str(env_file))

        expected = {"KEY1": "value1", "KEY2": "value2"}
        self.assertEqual(result, expected)

    def test_parse_env_file_not_found(self):
        """Test parsing non-existent file raises FileNotFoundError."""
        non_existent_file = Path(self.temp_dir) / "nonexistent.env"

        with self.assertRaises(FileNotFoundError):
            parse_env_file(str(non_existent_file))


class TestLoadEnvMcp(unittest.TestCase):
    """Tests for load_env_mcp function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.original_environ = os.environ.copy()

    def tearDown(self):
        """Clean up test fixtures."""
        # Restore original environment
        os.environ.clear()
        os.environ.update(self.original_environ)

        # Clean up temp directory
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_load_env_mcp_success(self):
        """Test successful loading of environment variables."""
        env_content = """
TEST_KEY=test_value
ANOTHER_KEY=another_value
"""
        env_file = Path(self.temp_dir) / ".env.mcp"
        env_file.write_text(env_content.strip())

        result = load_env_mcp(str(env_file))

        self.assertTrue(result)
        self.assertEqual(os.environ.get("TEST_KEY"), "test_value")
        self.assertEqual(os.environ.get("ANOTHER_KEY"), "another_value")

    def test_load_env_mcp_file_not_found(self):
        """Test loading when file is not found."""
        with patch("envmcp.core.find_env_file", return_value=None):
            result = load_env_mcp()

            self.assertFalse(result)

    def test_load_env_mcp_custom_path_not_found(self):
        """Test loading with custom path that doesn't exist."""
        non_existent_file = Path(self.temp_dir) / "nonexistent.env"

        result = load_env_mcp(str(non_existent_file))

        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
