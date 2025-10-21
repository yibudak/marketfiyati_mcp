# Contributing to Marketfiyati MCP

Thank you for your interest in contributing to Marketfiyati MCP! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/marketfiyati_mcp.git`
3. Create a new branch: `git checkout -b feature/your-feature-name`

## Development Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Making Changes

1. Write your code following the project's coding standards
2. Add tests for new functionality
3. Run tests locally:
   ```bash
   pytest
   ```

4. Format and lint your code:
   ```bash
   ruff check --fix app/ tests/
   ruff format app/ tests/
   ```

5. Ensure type checking passes:
   ```bash
   mypy app/ --ignore-missing-imports
   ```

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. The hooks will run automatically on commit and check:

- Code formatting and linting (ruff)
- Type checking (mypy)
- YAML/JSON validity
- Trailing whitespace
- Large files
- Merge conflicts

To run hooks manually:
```bash
pre-commit run --all-files
```

## Testing

- Write tests for all new features and bug fixes
- Ensure all tests pass before submitting a PR
- Aim for high test coverage (target: >80%)

Run tests with coverage:
```bash
pytest --cov=app --cov-report=term-missing
```

## Submitting Changes

1. Commit your changes with a clear commit message
2. Push to your fork
3. Create a Pull Request to the main repository
4. Wait for CI checks to pass
5. Address any review feedback

## Code Style

- Follow PEP 8 guidelines
- Use type hints for function parameters and return values
- Write docstrings for functions and classes
- Keep lines under 100 characters
- Use meaningful variable and function names

## Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Ensure CI/CD pipeline passes
- Keep PRs focused on a single feature or fix
- Update documentation if needed

## Questions?

If you have questions, please open an issue on GitHub.
