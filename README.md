# envmcp

[![PyPI version](https://img.shields.io/pypi/v/envmcp.svg)](https://pypi.org/project/envmcp/)
[![Python versions](https://img.shields.io/pypi/pyversions/envmcp.svg)](https://pypi.org/project/envmcp/)

Use environment variables in your Cursor MCP server definitions.

## Installation

```bash
pip install envmcp
```

## Recommended usage

Prefix your stdio command with `envmcp` and reference env vars by name in your cursor MCP config.

You can either pass the filepath of your env file as an argument...
```json
{
  "my_mcp_server": {
    "command": "envmcp",
    "args": [
      "--env-file",
      "/path/to/my.env.file",
      "python",
      "-m",
      "my_mcp_server",
      "$MY_NAMED_ENVIRONMENT_VARIABLE"
    ]
  },
  "example_with_shorthand_flag_name": {
    "command": "envmcp",
    "args": [
      "-e",
      "/path/to/my.env.file",
      "uvicorn",
      "app:app",
      "--host",
      "$HOST",
      "--port",
      "$PORT"
    ]
  }
}
```

... or put your secrets into a file called `.env.mcp` in your user's home directory, which will be looked up by default:
```json
{
  "my_mcp_server": {
    "command": "envmcp",
    "args": [
      "python",
      "-m",
      "my_mcp_server",
      "$MY_NAMED_ENVIRONMENT_VARIABLE"
    ]
  }
}
```

## What does it do?

Receives a shell command as input, loads environment variables from an env file, and then executes the command with those variables available in the environment.

## What's the point?

Store the secrets needed by your MCP server config in a file called `.env.mcp` in your home directory, and then replace this...

```json
{
  "my_database": {
    "command": "python",
    "args": [
      "-m",
      "my_mcp_server",
      "my secret connection string"
    ]
  },
  "my_other_mcp_server": {
    "command": "uvicorn",
    "args": ["app:app"],
    "env": {
      "MY_API_KEY": "my api key"
    }
  }
}
```

... with this:
```json
{
  "my_database": {
    "command": "envmcp",
    "args": [
      "python",
      "-m",
      "my_mcp_server",
      "$MY_DATABASE_CONNECTION_STRING"
    ]
  },
  "my_other_mcp_server": {
    "command": "envmcp",
    "args": [
      "uvicorn",
      "app:app",
      "--host",
      "$HOST"
    ]
  }
}
```

## Usage

```bash
envmcp [--env-file <path>] <command> [args...]
```

The tool will:
1. Look for a `.env.mcp` file in the current directory
2. If not found, it will search up the directory tree for a `.env.mcp` file
3. As a last resort, it will check for `~/.env.mcp`
4. If `--env-file` or `-e` is specified, it will use that file instead of searching
5. Load the environment variables from the found `.env.mcp` file
6. Execute the specified command with any provided arguments

### Options

- `--env-file <path>` or `-e <path>`: Specify a custom path to the environment file
- `--version`: Show version information
- `--help`: Show help message

## Environment File Format

The `.env.mcp` file follows the standard environment file format:

```
KEY=value
ANOTHER_KEY=another value
# This is a comment
QUOTED_VALUE="value with spaces"
```

See the `sample.env.mcp` file for a more detailed example.

## Python Examples

```bash
# Run a Python module with environment variables
envmcp python -m mypackage.server $API_KEY

# Start a FastAPI/Uvicorn server
envmcp uvicorn app:app --host $HOST --port $PORT

# Run pytest with test environment
envmcp python -m pytest --env $TEST_ENV

# Start Jupyter notebook
envmcp jupyter notebook --ip $JUPYTER_HOST

# Run Django management commands
envmcp python manage.py runserver $HOST:$PORT
```

## Contributing

Contributions are welcome: please feel free to open issues or PRs!

## Development

### Prerequisites

- Python 3.8 or later
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/lightfastai/envmcp-cursor.git
cd envmcp-cursor

# Install in development mode
pip install -e .

# Run tests
python -m unittest discover tests/
```

### Running Tests

```bash
# Run all tests
python -m unittest discover tests/

# Run specific test file
python -m unittest tests.test_core

# Run with coverage
pip install coverage
coverage run -m unittest discover tests/
coverage report
```

### Publishing

```bash
# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## License

MIT 
