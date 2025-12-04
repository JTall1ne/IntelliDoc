"""
IntelliDoc - Multi-Model AI Documentation Generator

IntelliDoc uses multiple AI models working in collaboration to generate
comprehensive, accurate, and maintainable code documentation.
"""

__version__ = "0.1.0"
__author__ = "JTall1ne"
__license__ = "Apache-2.0"

from intellidoc.core.orchestrator import MultiModelOrchestrator
from intellidoc.core.models import ModelProvider

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "MultiModelOrchestrator",
    "ModelProvider",
]
