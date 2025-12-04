# Contributing to IntelliDoc

Thank you for your interest in contributing to IntelliDoc! This document provides guidelines and instructions for contributing.

## 🌟 Ways to Contribute

- **Report bugs** and issues
- **Suggest new features** or improvements
- **Improve documentation**
- **Add support for new AI models**
- **Add support for new programming languages**
- **Implement new collaboration strategies**
- **Write tests**
- **Fix bugs**

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- API keys for at least one AI provider (OpenAI or Anthropic)

### Setup Development Environment

1. Fork the repository on GitHub

2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/IntelliDoc.git
cd IntelliDoc
```

3. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install in development mode with dev dependencies:
```bash
pip install -e ".[dev]"
```

5. Set up your API keys:
```bash
cp .env.template .env
# Edit .env with your API keys
```

6. Run tests to ensure everything works:
```bash
pytest
```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or changes

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add docstrings to functions and classes
- Add type hints where appropriate
- Update documentation if needed

### 3. Write Tests

All new features should include tests:

```python
# tests/test_your_feature.py
def test_your_feature():
    """Test description."""
    # Your test code
    assert expected == actual
```

Run tests:
```bash
pytest
pytest --cov=intellidoc  # With coverage
```

### 4. Format Your Code

We use Black for code formatting and Ruff for linting:

```bash
black intellidoc/ --line-length 100
ruff check intellidoc/
```

### 5. Commit Your Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Add support for GPT-4 Turbo model

- Added model configuration for GPT-4 Turbo
- Updated model provider to support new model
- Added tests for new model configuration
"
```

Commit message format:
- First line: Brief summary (50 chars or less)
- Blank line
- Detailed description (wrap at 72 chars)
- Reference issues: "Fixes #123"

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub:
- Provide a clear description of changes
- Reference related issues
- Include screenshots if relevant
- Ensure CI passes

## 🎯 Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints for function signatures
- Maximum line length: 100 characters
- Use docstrings for all public functions and classes

Example:
```python
from typing import List, Optional

def process_data(
    data: List[str],
    max_items: Optional[int] = None
) -> List[str]:
    """
    Process a list of data items.
    
    Args:
        data: List of strings to process
        max_items: Optional maximum number of items to process
        
    Returns:
        Processed list of strings
        
    Raises:
        ValueError: If data is empty
    """
    if not data:
        raise ValueError("Data cannot be empty")
    
    result = [item.strip() for item in data]
    
    if max_items:
        result = result[:max_items]
    
    return result
```

### Documentation Style

- Use Google-style docstrings
- Include type information in docstrings
- Provide examples for complex functions
- Keep documentation up-to-date with code

## 🏗️ Architecture Guidelines

### Adding a New AI Model Provider

1. Create provider class in `intellidoc/core/models.py`:

```python
class NewModelProvider(BaseModelProvider):
    """Provider for NewModel API."""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        # Initialize client
        
    async def generate(self, prompt: str, context: Optional[str] = None) -> ModelResponse:
        """Generate documentation using NewModel."""
        # Implementation
        
    def is_available(self) -> bool:
        """Check if provider is available."""
        # Implementation
```

2. Add to `ModelProvider` enum
3. Update `create_provider` factory function
4. Add configuration support
5. Write tests

### Adding a New Programming Language

1. Add language to `Language` enum in `parser.py`
2. Implement parser methods:
   - `_parse_language_name()`
   - `_extract_language_functions()`
   - `_extract_language_classes()`
3. Update `detect_language()` function
4. Add example file in `examples/`
5. Write tests

### Adding a New Collaboration Strategy

1. Add strategy to `CollaborationStrategy` enum
2. Implement strategy method in `MultiModelOrchestrator`:
   ```python
   async def _your_strategy_generation(self, task: DocumentationTask) -> CollaborationResult:
       """Your strategy description."""
       # Implementation
   ```
3. Update strategy dispatch in `generate_documentation()`
4. Document strategy in README
5. Write tests

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── test_smoke.py          # Basic import and sanity tests
├── test_core.py           # Core functionality tests
├── test_models.py         # Model provider tests
├── test_parser.py         # Code parser tests
├── test_orchestrator.py   # Orchestrator tests
└── test_integration.py    # End-to-end tests
```

### Writing Tests

- Use descriptive test names
- Test edge cases and error conditions
- Mock external API calls for unit tests
- Use fixtures for common setup
- Mark integration tests that require API keys

Example:
```python
import pytest
from unittest.mock import Mock, patch

def test_model_config_creation():
    """Test ModelConfig can be created with valid parameters."""
    config = ModelConfig(
        provider=ModelProvider.OPENAI,
        model_name="gpt-4"
    )
    assert config.provider == ModelProvider.OPENAI
    assert config.model_name == "gpt-4"

@pytest.mark.integration
@pytest.mark.asyncio
async def test_real_generation():
    """Test actual documentation generation (requires API keys)."""
    # This test is skipped in CI without API keys
    pass
```

## 📚 Documentation Guidelines

### Update Documentation When:

- Adding new features
- Changing existing functionality
- Adding new configuration options
- Adding examples
- Fixing bugs that affect documented behavior

### Documentation Locations:

- **README.md** - Main project documentation
- **CHANGELOG.md** - Record of all changes
- **Docstrings** - In-code documentation
- **examples/** - Usage examples
- **docs/** - Detailed documentation (future)

## 🐛 Reporting Bugs

### Before Submitting

- Check existing issues
- Test with latest version
- Verify it's not a configuration issue

### Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Configure with '...'
2. Run command '...'
3. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g. Ubuntu 22.04]
- Python version: [e.g. 3.11]
- IntelliDoc version: [e.g. 0.1.0]
- AI providers: [e.g. OpenAI, Anthropic]

**Additional context**
Any other relevant information.
```

## 💡 Suggesting Features

### Feature Request Template

```markdown
**Feature Description**
Clear description of the feature.

**Motivation**
Why this feature would be useful.

**Proposed Solution**
How you think it should work.

**Alternatives Considered**
Other approaches you've thought about.

**Additional Context**
Any other relevant information.
```

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Tests pass locally
- [ ] Code is formatted with Black
- [ ] Linting passes with Ruff
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Commit messages are clear

### PR Description Template

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing done:
- [ ] Unit tests added
- [ ] Integration tests added
- [ ] Manual testing performed

## Related Issues
Fixes #123
Related to #456

## Screenshots
If applicable, add screenshots.

## Checklist
- [ ] Tests pass
- [ ] Code is formatted
- [ ] Documentation updated
- [ ] CHANGELOG updated
```

## 🤝 Code Review Process

1. Maintainers review within 48 hours
2. Address feedback and push updates
3. Once approved, maintainer will merge
4. Your contribution will be in the next release!

## 📜 License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.

## 🙏 Recognition

Contributors will be recognized in:
- CHANGELOG.md
- README.md (for significant contributions)
- Release notes

## ❓ Questions?

- Open an issue with the "question" label
- Join discussions on GitHub Discussions
- Email: [contact information]

---

Thank you for contributing to IntelliDoc! Together we're building better documentation tools. 🚀
