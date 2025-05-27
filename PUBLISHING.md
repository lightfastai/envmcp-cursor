# Publishing Guide

This document explains how to set up automated publishing to PyPI using GitHub Actions.

## Prerequisites

1. **PyPI Account**: Create an account at [pypi.org](https://pypi.org)
2. **PyPI API Token**: Generate an API token in your PyPI account settings

## Setup Steps

### 1. Create PyPI API Token

1. Go to [PyPI Account Settings](https://pypi.org/manage/account/)
2. Scroll down to "API tokens" section
3. Click "Add API token"
4. Give it a name (e.g., "envmcp-github-actions")
5. Set scope to "Entire account" (or specific to this project once published)
6. Copy the generated token (starts with `pypi-`)

### 2. Add GitHub Secret

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI API token
6. Click "Add secret"

### 3. Publishing Process

The CI/CD pipeline is set up to automatically publish to PyPI when you create a GitHub release:

1. **Update version** in these files:
   - `pyproject.toml`
   - `envmcp/__init__.py`
   - `envmcp/cli.py`

2. **Create a Git tag**:
   ```bash
   git tag v0.1.0
   git push origin v0.1.0
   ```

3. **Create a GitHub Release**:
   - Go to your repository on GitHub
   - Click "Releases" → "Create a new release"
   - Choose the tag you just created
   - Fill in release title and description
   - Click "Publish release"

4. **Automatic Publishing**:
   - The GitHub Action will automatically trigger
   - It will build the package and publish to PyPI
   - Check the "Actions" tab to monitor progress

## Manual Publishing (Alternative)

If you prefer to publish manually:

```bash
# Install build tools
pip install build twine

# Build the package
python -m build

# Upload to PyPI
python -m twine upload dist/*
```

## Troubleshooting

- **Authentication Error**: Check that your PyPI API token is correctly set in GitHub secrets
- **Package Already Exists**: Make sure you've incremented the version number
- **Build Failures**: Check the GitHub Actions logs for detailed error messages

## Version Management

Follow semantic versioning (semver):
- `0.1.0` - Initial release
- `0.1.1` - Bug fixes
- `0.2.0` - New features (backward compatible)
- `1.0.0` - Major release (may include breaking changes) 