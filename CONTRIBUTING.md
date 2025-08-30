# Contributing to Bike Chatbot

Thank you for your interest in contributing to the Bike Chatbot project! This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Code Style](#code-style)
- [Documentation](#documentation)

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors. Please be respectful and considerate of others.

## Getting Started

1. **Fork the repository** on GitLab
2. **Clone your fork** locally
3. **Create a feature branch** for your changes
4. **Make your changes** following the guidelines below
5. **Test your changes** thoroughly
6. **Submit a merge request**

## Development Setup

### Prerequisites

- Python 3.9 or higher
- Git
- Docker (optional, for containerized development)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://gitlab.com/yourusername/bike-chatbot.git
   cd bike-chatbot
   ```

2. **Set up virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .\.venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # or for development
   pip install -e ".[dev]"
   ```

4. **Set up environment variables:**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   # or create a .env file
   echo "OPENAI_API_KEY=your-api-key-here" > .env
   ```

### Docker Development

```bash
docker-compose up -d
```

## Making Changes

### Branch Naming Convention

Use descriptive branch names:
- `feature/add-new-bike-category`
- `bugfix/fix-preference-parsing`
- `docs/update-readme`
- `refactor/improve-recommendation-algorithm`

### Commit Message Format

Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(bikes): add mountain bike category support
fix(intents): resolve budget parsing for values over 10k
docs(readme): update installation instructions
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_bikes.py

# Run with verbose output
pytest -v
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with `test_` prefix
- Use descriptive test function names
- Aim for high test coverage (target: >80%)

Example test:
```python
def test_recommend_bikes_with_budget():
    prefs = {"budget": 1000, "category": "city"}
    recommendations = recommend_bikes(prefs)
    assert len(recommendations) > 0
    assert all(r["price_usd"] <= 1000 for r in recommendations)
```

## Submitting Changes

1. **Push your changes** to your fork
2. **Create a merge request** on GitLab
3. **Use the provided template** for merge requests
4. **Link any related issues** in the merge request description
5. **Request review** from maintainers

### Merge Request Checklist

- [ ] Code follows style guidelines
- [ ] Tests pass and coverage is maintained
- [ ] Documentation is updated
- [ ] No new warnings are introduced
- [ ] Self-review completed

## Code Style

### Python Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking
- **isort** for import sorting

### Running Code Quality Tools

```bash
# Format code
black .

# Sort imports
isort .

# Lint code
ruff check .

# Type checking
mypy .

# Run all quality checks
ruff check . && black --check . && isort --check-only . && mypy .
```

### Pre-commit Hooks

Install pre-commit hooks for automatic code quality checks:

```bash
pip install pre-commit
pre-commit install
```

## Documentation

### Code Documentation

- Use docstrings for all public functions and classes
- Follow Google or NumPy docstring format
- Include type hints for function parameters and return values

Example:
```python
def recommend_bikes(prefs: Dict[str, Any], limit: int = 3) -> List[Dict[str, Any]]:
    """Recommend bikes based on user preferences.
    
    Args:
        prefs: Dictionary containing user preferences (budget, category, etc.)
        limit: Maximum number of recommendations to return
        
    Returns:
        List of bike dictionaries matching the preferences
    """
```

### Documentation Updates

When making changes that affect user-facing functionality:
- Update README.md if needed
- Add or update docstrings
- Update any relevant documentation files

## Getting Help

- **Issues**: Use the issue tracker for bugs and feature requests
- **Discussions**: Use GitLab discussions for questions and ideas
- **Documentation**: Check the README and inline documentation

## Recognition

Contributors will be recognized in:
- The project README
- Release notes
- GitLab contributors list

Thank you for contributing to Bike Chatbot! 🚲
