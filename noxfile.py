"""Nox configuration for lightfast-envmcp-cursor."""

import nox


# Default sessions to run when no session is specified
nox.options.sessions = ["lint", "type_check", "tests"]

PYTHON_VERSIONS = ["3.10", "3.11", "3.12", "3.13"]


@nox.session(python="3.13")  # Use latest Python for linting
def lint(session):
    """Run linting with ruff."""
    session.install("ruff")
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")


@nox.session(python="3.13")  # Use latest Python for type checking
def type_check(session):
    """Run type checking with mypy."""
    session.install("mypy")
    session.install("-e", ".")
    session.run("mypy", "envmcp")


@nox.session(python=PYTHON_VERSIONS)
def tests(session):
    """Run the test suite."""
    session.install("-e", ".")
    session.install("pytest", "pytest-cov", "pytest-xdist")
    # Pass through any additional arguments to pytest
    session.run("pytest", "tests/", "-v", *session.posargs)


@nox.session(python="3.13")
def format(session):
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", ".")
    session.run("ruff", "check", "--fix", ".")


@nox.session(python="3.13")
def coverage(session):
    """Run tests with coverage reporting."""
    session.install("-e", ".")
    session.install("pytest", "pytest-cov", "coverage")
    session.run(
        "pytest",
        "tests/",
        "--cov=envmcp",
        "--cov-report=term-missing",
        "--cov-report=xml",
    )


@nox.session(python="3.13")
def build(session):
    """Build the package."""
    session.install("build")
    session.run("python", "-m", "build")


@nox.session(python=PYTHON_VERSIONS)
def cli_test(session):
    """Test CLI functionality."""
    session.install("-e", ".")

    # Test help command
    session.run("envmcp", "--help")

    # Test version command
    session.run("envmcp", "--version")

    # Test with a simple command
    session.run("sh", "-c", "echo 'TEST_VAR=hello' > test.env", external=True)
    session.run(
        "envmcp",
        "--env-file",
        "test.env",
        "python",
        "-c",
        "import os; print('TEST_VAR:', os.environ.get('TEST_VAR', 'NOT_FOUND'))",
    )
    session.run("rm", "-f", "test.env", external=True)


@nox.session(python="3.13")
def security(session):
    """Run security checks."""
    session.install("-e", ".")
    session.install("bandit[toml]")

    # Run bandit security scan on source code
    session.run(
        "bandit",
        "-r",
        "envmcp/",
        "-f",
        "txt",
        success_codes=[0, 1],
    )


@nox.session(python="3.13")
def safety_check(session):
    """Run safety check on dependencies (separate session due to potential hanging)."""
    session.install("-e", ".")
    session.install("safety")

    # Run safety check on dependencies
    session.run("safety", "scan", "--output", "text", success_codes=[0, 1])


@nox.session(python="3.13")
def dev(session):
    """Set up development environment."""
    session.install("-e", ".")
    session.install(
        "ruff",
        "mypy",
        "pytest",
        "pytest-cov",
        "pytest-xdist",
        "coverage",
        "build",
        "safety",
        "bandit[toml]",
    )
    session.log("Development environment ready!")
    session.log("Available commands:")
    session.log("  nox -s lint      # Run linting")
    session.log("  nox -s format    # Format code")
    session.log("  nox -s tests     # Run tests")
    session.log("  nox -s coverage  # Run tests with coverage")
    session.log("  nox -s type_check # Run type checking")
    session.log("  nox -s security  # Run security checks")
