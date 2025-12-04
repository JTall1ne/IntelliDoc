"""
Smoke tests to verify basic functionality.
"""

def test_import_intellidoc():
    """Test that intellidoc package can be imported."""
    import intellidoc
    assert intellidoc is not None


def test_version_exists():
    """Test that version is defined."""
    from intellidoc import __version__
    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_core_imports():
    """Test that core modules can be imported."""
    from intellidoc.core import (
        MultiModelOrchestrator,
        ModelProvider,
        CodeParser,
        Language,
        detect_language
    )
    assert MultiModelOrchestrator is not None
    assert ModelProvider is not None
    assert CodeParser is not None
    assert Language is not None
    assert detect_language is not None


def test_cli_imports():
    """Test that CLI can be imported."""
    from cli.main import app
    assert app is not None


def test_api_imports():
    """Test that API can be imported."""
    from api.app import app
    assert app is not None


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
