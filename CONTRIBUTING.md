# Contributing to ASA Starter Kit

Thank you for your interest in contributing to the ASA Starter Kit! This document provides guidelines and instructions for contributing.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Setup](#development-setup)
4. [ASA Architecture Rules](#asa-architecture-rules)
5. [Code Style](#code-style)
6. [Testing](#testing)
7. [Submitting Changes](#submitting-changes)
8. [Reporting Issues](#reporting-issues)

---

## Code of Conduct

This project follows a simple code of conduct:

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Keep discussions professional

---

## Getting Started

### Prerequisites

- Python 3.11 or higher
- Git
- Familiarity with FastAPI and Pydantic
- Understanding of ASA architecture principles

### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR_USERNAME/asa-starter-kit.git
cd asa_starter_kit

# Add upstream remote
git remote add upstream https://github.com/vibecodiq/asa-starter-kit.git
```

---

## Development Setup

### Option 1: With Devbox (Recommended)

```bash
# Install devbox
curl -fsSL https://get.jetpack.io/devbox | bash

# Start devbox shell
devbox shell

# Dependencies are automatically installed
```

### Option 2: Without Devbox

```bash
# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-asyncio pytest-cov ruff mypy
```

### Verify Setup

```bash
# Run tests
pytest

# Run linters
ruff check .
mypy .

# Start server
python main.py
```

---

## ASA Architecture Rules

When contributing, follow these ASA principles:

### 1. Slice Independence

- Each slice must be self-contained
- No direct imports between slices
- Use shared modules for common functionality

### 2. Required Files

Every slice must have:
- `slice.spec.md` - Functional specification
- `slice.contract.json` - API contract
- `handler.py` - FastAPI route handler
- `service.py` - Business logic
- `repository.py` - Data access
- `schemas.py` - Pydantic models
- `tests/test_slice.py` - Tests
- `__init__.py` - Package marker

### 3. LOC Limits

- `handler.py`: ≤ 150 lines
- `service.py`: ≤ 200 lines
- `repository.py`: ≤ 150 lines
- `schemas.py`: ≤ 100 lines
- `test_slice.py`: ≤ 300 lines

### 4. Import Rules

Allowed imports:
- Own slice modules: `domains.{domain}.slices.{slice_name}.*`
- Shared modules: `shared.*`
- External libraries: As declared in `slice.contract.json`

Forbidden imports:
- Other slices
- Main application modules
- Orchestrator modules

### 5. Naming Conventions

- **Slices:** `snake_case` (e.g., `login_demo`, `update_profile`)
- **Classes:** `PascalCase` (e.g., `LoginDemoHandler`, `UpdateProfileService`)
- **Functions:** `snake_case` (e.g., `hash_password`, `create_token`)
- **Files:** `snake_case.py` (e.g., `handler.py`, `test_slice.py`)

---

## Code Style

### Python Style

We use **Ruff** for linting and formatting:

```bash
# Check code
ruff check .

# Format code
ruff format .
```

### Code Style Rules

- Line length: 100 characters
- Use type hints for all functions
- Write docstrings for public functions
- Follow PEP 8 conventions

### Example

```python
"""Module docstring"""
from typing import Optional
from pydantic import BaseModel


class UserRequest(BaseModel):
    """User request schema"""
    email: str
    password: str


async def authenticate_user(email: str, password: str) -> Optional[dict]:
    """
    Authenticate user with email and password.

    Args:
        email: User email address
        password: User password

    Returns:
        User data if authenticated, None otherwise
    """
    # Implementation here
    pass
```

---

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov

# Run specific test file
pytest tests/test_asa_linters.py

# Run specific test
pytest tests/test_cli.py::test_list_slices -v
```

### Writing Tests

- Use `pytest` for all tests
- Use `pytest-asyncio` for async tests
- Aim for >80% code coverage
- Test both success and failure cases

### Test Structure

```python
"""Tests for feature X"""
import pytest
from fastapi.testclient import TestClient


def test_feature_success():
    """Test successful case"""
    # Arrange
    # Act
    # Assert
    pass


def test_feature_failure():
    """Test failure case"""
    # Arrange
    # Act
    # Assert
    pass
```

---

## Submitting Changes

### Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages

Follow conventional commits:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

Examples:
```
feat(cli): add generate-slice command
fix(linter): correct LOC count for multiline strings
docs(readme): update installation instructions
```

### Pull Request Process

1. **Create a branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make your changes**
   - Follow code style guidelines
   - Add tests for new features
   - Update documentation

3. **Run quality checks**
   ```bash
   # Run tests
   pytest
   
   # Run linters
   ruff check .
   mypy .
   
   # Run ASA linters
   asa lint-all
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature
   ```

6. **Create Pull Request**
   - Go to GitHub
   - Click "New Pull Request"
   - Fill in the PR template
   - Link related issues

### Pull Request Checklist

- [ ] Tests pass (`pytest`)
- [ ] Linters pass (`ruff check .`)
- [ ] Type checks pass (`mypy .`)
- [ ] ASA linters pass (`asa lint-all`)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)
- [ ] Commit messages follow conventions

---

## Reporting Issues

### Bug Reports

Include:
- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages/stack traces

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Additional context

### Issue Template

```markdown
**Description:**
Brief description of the issue

**Steps to Reproduce:**
1. Step one
2. Step two
3. ...

**Expected Behavior:**
What should happen

**Actual Behavior:**
What actually happens

**Environment:**
- Python version: 3.11.x
- OS: Ubuntu 22.04
- ASA version: v0.9.0

**Additional Context:**
Any other relevant information
```

---

## Questions?

- **Documentation**: Check [GETTING_STARTED.md](GETTING_STARTED.md)
- **Issues**: [GitHub Issues](https://github.com/vibecodiq/asa-starter-kit/issues)
- **Email**: jan@vibecodiq.com

---

**ASA Starter Kit v0.9.0**  
Copyright © 2025 Jan Voldán, VibeCodiq  
Licensed under the MIT License

Thank you for contributing! 🚀
