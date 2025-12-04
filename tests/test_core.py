"""
Comprehensive test suite for IntelliDoc core functionality.
"""

import pytest
from intellidoc.core import (
    ModelProvider,
    ModelConfig,
    DocumentationTask,
    CollaborationStrategy,
    Language,
    CodeParser,
    detect_language,
)


class TestLanguageDetection:
    """Test language detection from filenames."""

    def test_python_detection(self):
        assert detect_language("test.py") == Language.PYTHON
        assert detect_language("module.py") == Language.PYTHON

    def test_javascript_detection(self):
        assert detect_language("script.js") == Language.JAVASCRIPT
        assert detect_language("component.jsx") == Language.JAVASCRIPT

    def test_typescript_detection(self):
        assert detect_language("app.ts") == Language.TYPESCRIPT
        assert detect_language("component.tsx") == Language.TYPESCRIPT

    def test_java_detection(self):
        assert detect_language("Main.java") == Language.JAVA

    def test_unknown_extension(self):
        assert detect_language("file.unknown") is None
        assert detect_language("README.md") is None


class TestCodeParser:
    """Test code parsing functionality."""

    def test_parse_python_function(self):
        code = '''
def hello_world(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"
'''
        parser = CodeParser(Language.PYTHON)
        elements = parser.parse_file(code)
        
        assert len(elements) > 0
        func = elements[0]
        assert func.type == "function"
        assert func.name == "hello_world"
        assert "hello_world" in func.code

    def test_parse_python_class(self):
        code = '''
class Calculator:
    """A simple calculator class."""
    
    def add(self, a: int, b: int) -> int:
        """Add two numbers."""
        return a + b
'''
        parser = CodeParser(Language.PYTHON)
        elements = parser.parse_file(code)
        
        # Should find the class
        classes = [e for e in elements if e.type == "class"]
        assert len(classes) > 0
        assert classes[0].name == "Calculator"


class TestModelConfig:
    """Test model configuration."""

    def test_openai_config_creation(self):
        config = ModelConfig(
            provider=ModelProvider.OPENAI,
            model_name="gpt-4",
            api_key="test-key",
            temperature=0.7
        )
        assert config.provider == ModelProvider.OPENAI
        assert config.model_name == "gpt-4"
        assert config.temperature == 0.7

    def test_anthropic_config_creation(self):
        config = ModelConfig(
            provider=ModelProvider.ANTHROPIC,
            model_name="claude-3-5-sonnet-20241022",
            api_key="test-key"
        )
        assert config.provider == ModelProvider.ANTHROPIC


class TestDocumentationTask:
    """Test documentation task creation."""

    def test_task_creation(self):
        task = DocumentationTask(
            code="def test(): pass",
            language="python",
            context="Test function"
        )
        assert task.code == "def test(): pass"
        assert task.language == "python"
        assert task.context == "Test function"
        assert task.doc_type == "general"


class TestCollaborationStrategy:
    """Test collaboration strategies."""

    def test_strategy_values(self):
        assert CollaborationStrategy.CONSENSUS.value == "consensus"
        assert CollaborationStrategy.SPECIALIZATION.value == "specialization"
        assert CollaborationStrategy.REVIEW.value == "review"
        assert CollaborationStrategy.VOTING.value == "voting"


# Integration tests (require API keys, marked for optional execution)
@pytest.mark.integration
@pytest.mark.asyncio
async def test_orchestrator_initialization():
    """Test orchestrator can be initialized (requires valid config)."""
    from intellidoc.core import load_config, MultiModelOrchestrator
    
    try:
        config = load_config()
        if config.models:
            orchestrator = MultiModelOrchestrator(config.models)
            assert len(orchestrator.providers) > 0
    except Exception:
        pytest.skip("No valid API configuration found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
