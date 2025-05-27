# Contributing to envmcp

Thank you for your interest in contributing to envmcp! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8 or later
- Git

### Setup

1. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/lightfastai/envmcp-cursor.git
   cd envmcp-cursor
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**:
   ```bash
   pip install -e .
   pip install -r requirements-dev.txt
   ```

## Development Workflow

### Code Quality

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
# Format code
black .
isort .

# Check linting
flake8 envmcp tests

# Type checking
mypy envmcp --ignore-missing-imports
```

### Testing

Run the test suite:
```bash
# Run all tests
python -m unittest discover tests/ -v

# Run with coverage
coverage run -m unittest discover tests/
coverage report
```

### Manual Testing

Test the CLI functionality:
```bash
# Test help
envmcp --help

# Test with a sample env file
echo "TEST_VAR=hello" > test.env
envmcp --env-file test.env python -c "import os; print(os.environ.get('TEST_VAR'))"
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
# Run tests
python -m unittest discover tests/ -v

# Run linting
black --check .
isort --check-only .
flake8 envmcp tests
mypy envmcp --ignore-missing-imports
```

### 4. Commit and Push

```bash
git add .
git commit -m "Add your descriptive commit message"
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

- Go to GitHub and create a pull request
- Describe your changes clearly
- Link any related issues

## Code Style Guidelines

- Follow PEP 8 (enforced by flake8)
- Use type hints for all functions
- Write docstrings for public functions
- Keep line length to 88 characters (Black default)
- Use descriptive variable and function names

## Testing Guidelines

- Write tests for all new functionality
- Aim for high test coverage
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

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

## Questions?

Feel free to open an issue for questions or discussion about potential contributions.

Thank you for contributing! 🎉 