"""Nox configuration for envmcp."""

import nox


# Python versions to test against
PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12", "3.13"]
# Default Python version for development
DEFAULT_PYTHON = "3.13"


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    session.install("uv")
    session.run("uv", "pip", "install", "-e", ".")
    session.run("uv", "pip", "install", "pytest", "pytest-cov")
    session.run("pytest", "tests/", "-v")


@nox.session(python=DEFAULT_PYTHON)
def lint(session):
    """Run linting with ruff."""
    session.install("uv")
    session.run("uv", "pip", "install", "ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python=DEFAULT_PYTHON)
def format(session):
    """Format code with ruff."""
    session.install("uv")
    session.run("uv", "pip", "install", "ruff")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", "--fix", ".")


@nox.session(python=DEFAULT_PYTHON)
def type_check(session):
    """Run type checking with mypy."""
    session.install("uv")
    session.run("uv", "pip", "install", "-e", ".")
    session.run("uv", "pip", "install", "mypy")
    session.run("mypy", "envmcp")


@nox.session(python=DEFAULT_PYTHON)
def coverage(session):
    """Run tests with coverage reporting."""
    session.install("uv")
    session.run("uv", "pip", "install", "-e", ".")
    session.run("uv", "pip", "install", "pytest", "pytest-cov", "coverage")
    session.run(
        "pytest",
        "tests/",
        "--cov=envmcp",
        "--cov-report=term-missing",
        "--cov-report=xml",
    )


@nox.session(python=DEFAULT_PYTHON)
def build(session):
    """Build the package."""
    session.install("uv")
    session.run("uv", "pip", "install", "build")
    session.run("python", "-m", "build")


@nox.session(python=DEFAULT_PYTHON)
def cli_test(session):
    """Test CLI functionality."""
    session.install("uv")
    session.run("uv", "pip", "install", "-e", ".")

    # Test help command
    session.run("envmcp", "--help")

    # Test version command
    session.run("envmcp", "--version")

    # Test with a simple command
    session.run("sh", "-c", "echo 'TEST_VAR=hello' > test.env")
    session.run(
        "envmcp",
        "--env-file",
        "test.env",
        "python",
        "-c",
        "import os; print('TEST_VAR:', os.environ.get('TEST_VAR', 'NOT_FOUND'))",
    )
    session.run("rm", "-f", "test.env")


@nox.session(python=DEFAULT_PYTHON)
def dev(session):
    """Set up development environment."""
    session.install("uv")
    session.run("uv", "pip", "install", "-e", ".")
    session.run(
        "uv",
        "pip",
        "install",
        "ruff",
        "mypy",
        "pytest",
        "pytest-cov",
        "coverage",
        "build",
    )
    session.log("Development environment ready!")
    session.log("Available commands:")
    session.log("  nox -s lint      # Run linting")
    session.log("  nox -s format    # Format code")
    session.log("  nox -s tests     # Run tests")
    session.log("  nox -s coverage  # Run tests with coverage")
    session.log("  nox -s type_check # Run type checking")
