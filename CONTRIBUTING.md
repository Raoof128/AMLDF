# Contributing to AMLD-F

Thank you for your interest in contributing to the **Adversarial Machine Learning Defense Framework (AMLD-F)**! We welcome contributions from the community to help make AI systems more robust, secure, and resilient.

This document provides guidelines for contributing to the project. Please take a moment to review this information before submitting contributions.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Pull Request Process](#pull-request-process)
- [Safety & Ethics](#safety--ethics)
- [Issue Reporting](#issue-reporting)

---

## 🤝 Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it to understand the expectations for all contributors.

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9+**
- **Git**
- **Make** (optional, but recommended)
- Familiarity with PyTorch, FastAPI, and adversarial ML concepts

### Setup Your Development Environment

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/AMLD-F.git
   cd AMLD-F
   ```

3. **Set up upstream remote**:
   ```bash
   git remote add upstream https://github.com/original-owner/AMLD-F.git
   ```

4. **Install dependencies**:
   ```bash
   # Using Make (recommended)
   make install
   
   # Or manually
   pip install -r requirements.txt
   pip install -e .[dev]
   ```

5. **Verify your setup**:
   ```bash
   make test
   ```

---

## 🔄 Development Workflow

### 1. Create a Feature Branch

```bash
# Update your fork
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/descriptive-name
# OR for bugfixes
git checkout -b fix/issue-number-description
```

**Branch Naming Conventions:**
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test improvements

### 2. Make Your Changes

- Write clean, readable code
- Follow the [Coding Standards](#coding-standards)
- Add tests for new functionality
- Update documentation as needed

### 3. Format and Lint

**Before committing**, ensure your code meets quality standards:

```bash
# Format code
make format

# Check linting
make lint

# Type check (optional, but recommended)
make typecheck
```

### 4. Run Tests

```bash
# Run all tests
make test

# Run with coverage
make test-cov

# Run specific test file
python3 -m pytest tests/test_api.py -v
```

**All tests must pass before submitting a PR.**

### 5. Commit Your Changes

Follow **conventional commits** format:

```bash
git add .
git commit -m "feat: add new PGD attack variant"
# OR
git commit -m "fix: resolve FGSM epsilon boundary issue"
# OR
git commit -m "docs: update API reference for drift detection"
```

**Commit Message Prefixes:**
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `style:` - Code style (formatting, no logic change)
- `refactor:` - Code restructuring
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks

### 6. Push and Create PR

```bash
git push origin feature/descriptive-name
```

Then create a Pull Request on GitHub.

---

## 📝 Coding Standards

### Python Style

- **Formatter**: [Black](https://github.com/psf/black) (88 character line length)
- **Import Sorting**: [isort](https://github.com/PyCQA/isort)
- **Linter**: [flake8](https://flake8.pycqa.org/)
- **Type Checker**: [mypy](https://mypy.readthedocs.io/) (optional)

### Code Quality Requirements

#### 1. Type Hints

All functions must have type hints:

```python
# Good ✅
def calculate_perturbation(
    data: torch.Tensor, 
    epsilon: float
) -> torch.Tensor:
    return data * epsilon

# Bad ❌
def calculate_perturbation(data, epsilon):
    return data * epsilon
```

#### 2. Docstrings

Use **Google-style docstrings** for all public modules, classes, and functions:

```python
def run_attack(
    model: torch.nn.Module,
    data: torch.Tensor,
    epsilon: float = 0.1
) -> Dict[str, Any]:
    """
    Execute the FGSM attack on the given model.

    Args:
        model: The PyTorch model to attack.
        data: Input tensor of shape (batch, channels, height, width).
        epsilon: Perturbation magnitude (default: 0.1).

    Returns:
        Dictionary containing:
            - adversarial_data: The perturbed input.
            - perturbation: The noise added.
            - success: Whether the attack succeeded.

    Raises:
        ValueError: If epsilon is negative or data shape is invalid.
    
    Example:
        >>> model = SimpleCNN()
        >>> data = torch.rand(1, 1, 28, 28)
        >>> result = run_attack(model, data, epsilon=0.1)
    """
    ...
```

#### 3. Error Handling

All public functions should handle errors gracefully:

```python
# Good ✅
try:
    result = attacker.run(data, target, epsilon=epsilon)
    logger.info(f"Attack executed successfully")
    return result
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise HTTPException(status_code=400, detail=str(e))
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

#### 4. Logging

Use the centralized logger:

```python
from backend.utils.logger import logger

logger.info("Operation completed successfully")
logger.warning("Potential issue detected")
logger.error("Operation failed")
```

---

## 🧪 Testing Guidelines

### Test Requirements

- **All new features** must include unit tests
- **All bug fixes** should include a regression test
- **Maintain or improve** overall code coverage (target: ≥75%)
- **Tests must pass** before PR approval

### Writing Tests

#### Unit Tests

Place unit tests in `tests/test_engines.py`:

```python
def test_new_attack():
    """Test the new attack implementation."""
    model = SimpleCNN()
    attacker = NewAttack(model)
    data = torch.rand(1, 1, 28, 28)
    target = torch.tensor([0])
    
    result = attacker.run(data, target)
    
    assert "adversarial_data" in result
    assert result["adversarial_data"].shape == data.shape
```

#### API Tests

Place API tests in `tests/test_api.py`:

```python
def test_new_endpoint():
    """Test the new API endpoint."""
    response = client.post("/attack/new", json={"param": "value"})
    assert response.status_code == 200
    assert "result" in response.json()
```

### Running Tests

```bash
# Run all tests
make test

# Run with verbose output
python3 -m pytest -v

# Run specific test
python3 -m pytest tests/test_api.py::test_health_check -v

# Run with coverage
make test-cov
```

---

## 📚 Documentation Guidelines

### Required Documentation

When adding new features, update:

1. **Code Docstrings**: Inline documentation
2. **API Reference**: `docs/API.md` (if adding new endpoints)
3. **Architecture Docs**: `docs/ARCHITECTURE.md` (if changing architecture)
4. **README**: Main `README.md` (if adding major features)
5. **CHANGELOG**: `CHANGELOG.md` (for all changes)

### Documentation Style

- Use **clear, concise language**
- Include **code examples** where applicable
- Use **proper markdown formatting**
- Add **diagrams** for complex concepts (Mermaid preferred)

---

## 🔁 Pull Request Process

### Before Submitting

Ensure your PR:
- [ ] Passes all tests (`make test`)
- [ ] Follows code style (`make format` and `make lint`)
- [ ] Includes documentation updates
- [ ] Has a clear, descriptive title
- [ ] References related issues (if applicable)

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring

## Related Issues
Closes #123

## Testing
Describe the tests you ran and how to reproduce.

## Checklist
- [ ] Tests pass locally
- [ ] Code is formatted (`make format`)
- [ ] Code is linted (`make lint`)
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

### Review Process

1. **Automated Checks**: CI/CD pipeline runs tests
2. **Code Review**: Maintainer reviews code
3. **Feedback**: Address any requested changes
4. **Approval**: PR is approved and merged

---

## 🔒 Safety & Ethics

### Ethical Guidelines

**DO:**
- ✅ Submit code for defensive AI research
- ✅ Create safe, simulated attacks
- ✅ Improve model robustness
- ✅ Enhance detection capabilities
- ✅ Add educational content

**DO NOT:**
- ❌ Submit code for real-world exploitation
- ❌ Include malicious payloads or backdoors
- ❌ Add features that enable unauthorized access
- ❌ Violate any laws or regulations
- ❌ Bypass safety mechanisms

### Attack Submissions

All attack implementations must:
- Run on **synthetic/dummy data only**
- Be **clearly documented** as educational
- Include **safety warnings** in docstrings
- Have **no real-world harm potential**

**Violations of these guidelines will result in immediate PR rejection.**

---

## 🐛 Issue Reporting

### Before Creating an Issue

1. **Search existing issues** to avoid duplicates
2. **Verify** the issue exists in the latest version
3. **Collect relevant information** (error logs, steps to reproduce)

### Creating an Issue

Use the appropriate template:

**Bug Report:**
```markdown
## Description
Clear description of the bug.

## Steps to Reproduce
1. Step 1
2. Step 2
3. See error

## Expected Behavior
What should happen.

## Actual Behavior
What actually happens.

## Environment
- OS: macOS 14.0
- Python: 3.10
- AMLD-F Version: 1.0.0
```

**Feature Request:**
```markdown
## Feature Description
What feature do you want?

## Use Case
Why is this feature useful?

## Proposed Implementation
How might this work? (optional)
```

---

## 🙏 Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md` (if created)
- Mentioned in release notes
- Credited in the repository

---

## 📬 Questions?

- **General Questions**: [GitHub Discussions](https://github.com/your-username/AMLD-F/discussions)
- **Bug Reports**: [GitHub Issues](https://github.com/your-username/AMLD-F/issues)
- **Security Issues**: See [SECURITY.md](SECURITY.md)

---

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<div align="center">

**Thank you for contributing to AMLD-F!** 🎉

Together, we're making AI systems more secure and robust.

</div>
