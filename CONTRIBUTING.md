# Contributing to envmcp

Thank you for your interest in contributing to envmcp! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.10 or later (3.13.3 recommended)
- Git
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

### Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/lightfastai/envmcp-cursor.git
   cd envmcp-cursor
   ```

2. **Install development dependencies**:
   
   **With uv (recommended)**:
   ```bash
   uv sync --group dev
   ```
   
   **Or with pip**:
   ```bash
   pip install -e .[dev]
   ```

## Development Workflow

### Code Quality

We use modern Python tooling to maintain code quality:

- **ruff**: Fast linting and code formatting (replaces black, flake8, isort)
- **mypy**: Type checking
- **nox**: Task automation and testing across Python versions

### Using Nox (Recommended)

This project uses [nox](https://nox.thea.codes/) for task automation:

```bash
# Set up development environment
nox -s dev

# Run linting and formatting
nox -s lint
nox -s format

# Run tests on all supported Python versions
nox -s tests

# Run tests on specific Python version
nox -s tests --python 3.13

# Run type checking
nox -s type_check

# Run tests with coverage
nox -s coverage

# Test CLI functionality
nox -s cli_test

# Build package
nox -s build
```

### Manual Commands

If you prefer to run tools directly:

```bash
# Format code
ruff format .
ruff check --fix .

# Check linting (without fixing)
ruff check .
ruff format --check .

# Type checking
mypy envmcp

# Run tests
pytest tests/

# Run tests with coverage
pytest tests/ --cov=envmcp --cov-report=term-missing
```

### Testing

Run the test suite:
```bash
# Using nox (recommended)
nox -s tests

# Or manually
pytest tests/ -v

# With coverage
nox -s coverage
```

### Manual CLI Testing

Test the CLI functionality:
```bash
# Using nox
nox -s cli_test

# Or manually
envmcp --help
echo "TEST_VAR=hello" > test.env
envmcp --env-file test.env python -c "import os; print(os.environ.get('TEST_VAR'))"
rm test.env
```

## Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write clear, concise code
- Add tests for new functionality
- Update documentation if needed
- Follow the existing code style

### 3. Test Your Changes

```bash
# Run all checks with nox (recommended)
nox -s lint
nox -s tests
nox -s type_check

# Or run manually
ruff check .
ruff format --check .
pytest tests/ -v
mypy envmcp
```

### 4. Commit and Push

```bash
git add .
git commit -m "Add your descriptive commit message"
git push origin username/your-feature-name
```

### 5. Create a Pull Request

- Go to GitHub and create a pull request
- Describe your changes clearly
- Link any related issues

## Code Style Guidelines

- Follow PEP 8 (enforced by ruff)
- Use type hints for all functions
- Write docstrings for public functions
- Keep line length to 88 characters (ruff default)
- Use descriptive variable and function names
- Code is automatically formatted with ruff (replaces black, isort, flake8)

## Testing Guidelines

- Write tests for all new functionality using pytest
- Aim for high test coverage
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies
- Run tests across all supported Python versions with `nox -s tests`

## Documentation

- Update README.md if you add new features
- Add docstrings to new functions
- Update type hints
- Consider adding examples for new functionality

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages (if any)
- Output of `envmcp --version`

## Development Tools

This project uses modern Python development tools:

- **nox**: Task automation and testing across Python versions
- **ruff**: Fast linting and formatting (replaces black, flake8, isort)
- **mypy**: Static type checking
- **pytest**: Testing framework
- **uv**: Fast Python package installer (optional but recommended)

All tools are configured in `pyproject.toml` and `ruff.toml`.

## Questions?

Feel free to open an issue for questions or discussion about potential contributions.

Thank you for contributing! 🎉 