# IntelliDoc

> **Multi-Model AI Documentation Generator**

IntelliDoc leverages multiple AI models working in collaboration to automatically generate high-quality, comprehensive code documentation. Rather than relying on a single AI model, IntelliDoc orchestrates multiple models (GPT-4, Claude, and more) to combine their unique strengths and produce superior documentation.

## 🌟 Key Features

- **Multi-Model Collaboration** - Multiple AI models work together, each contributing their strengths
- **Four Collaboration Strategies** - Choose how models work together:
  - **Consensus**: Models generate independently, outputs are intelligently merged
  - **Specialization**: Different models handle different aspects (overview, technical details, examples)
  - **Review**: One model generates, others review and improve
  - **Voting**: Models generate independently, best output is selected
- **Multi-Language Support** - Python, JavaScript, TypeScript, Java, C++, Go, Rust, and more
- **Intelligent Code Parsing** - Uses tree-sitter for accurate code analysis
- **CLI & API** - Use via command line or integrate into your applications
- **Git Integration** - Automatically update documentation on code changes
- **Extensible Architecture** - Easy to add new models or customize behavior

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/IntelliDoc.git
cd IntelliDoc

# Install dependencies
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

### Configuration

1. Initialize IntelliDoc in your project:

```bash
intellidoc init
```

2. Set your API keys:

```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

Or create a `.env` file (copy from `.env.template`):

```bash
cp .env.template .env
# Edit .env with your API keys
```

3. Customize settings in `.intellidoc.yml`:

```yaml
# Multi-model configuration
openai:
  enabled: true
  model: gpt-4
  temperature: 0.7

anthropic:
  enabled: true
  model: claude-3-5-sonnet-20241022
  temperature: 0.7

# Collaboration strategy
strategy: consensus  # consensus, specialization, review, or voting
```

### Usage

#### Command Line

Generate documentation for a single file:

```bash
intellidoc generate path/to/your/code.py
```

Save output to a file:

```bash
intellidoc generate path/to/your/code.py --output docs/code_doc.md
```

Use a specific collaboration strategy:

```bash
intellidoc generate path/to/your/code.py --strategy specialization
```

Show available models and configuration:

```bash
intellidoc info
```

#### API Server

Start the API server:

```bash
uvicorn api.app:app --reload
```

Generate documentation via API:

```bash
curl -X POST "http://localhost:8000/docs/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(name):\n    return f\"Hello, {name}!\"",
    "language": "python"
  }'
```

View API documentation at: http://localhost:8000/docs

## 🧠 Multi-Model Collaboration Explained

IntelliDoc's key innovation is **multi-model collaboration**. Instead of relying on a single AI model, multiple models work together to generate better documentation.

### Why Multi-Model?

Different AI models have different strengths:
- **GPT-4**: Excellent at high-level explanations and natural language
- **Claude**: Strong at technical accuracy and code analysis
- **Local models**: Privacy-preserving, customizable for domain-specific needs

By combining models, IntelliDoc produces documentation that is:
- More accurate (models cross-validate each other)
- More comprehensive (different perspectives are included)
- More reliable (reduced hallucination through consensus)

### Collaboration Strategies

#### 1. Consensus Strategy (Default)
All models generate documentation independently, then their outputs are intelligently merged to create a comprehensive result that incorporates the best aspects of each.

**Best for**: General documentation where you want comprehensive coverage

#### 2. Specialization Strategy
Different models are assigned specific tasks:
- Model 1: High-level overview and architecture
- Model 2: Technical implementation details
- Model 3: Usage examples and best practices

**Best for**: Complex code requiring different types of documentation

#### 3. Review Strategy
A primary model generates initial documentation, then other models review and suggest improvements.

**Best for**: When you have a preferred primary model but want quality assurance

#### 4. Voting Strategy
All models generate documentation independently, then the best output is selected based on multiple quality criteria.

**Best for**: Simple code where you want the single best explanation

## 📚 Architecture

```
intellidoc/
├── core/
│   ├── models.py         # Model provider abstraction (OpenAI, Anthropic, local)
│   ├── orchestrator.py   # Multi-model coordination and collaboration
│   ├── parser.py         # Code parsing with tree-sitter
│   └── config.py         # Configuration management
├── cli/
│   └── main.py          # Command-line interface
├── api/
│   ├── app.py           # FastAPI application
│   └── routers/
│       └── docs.py      # API endpoints
└── tests/               # Comprehensive test suite
```

## 🔧 Advanced Usage

### Custom Model Configuration

Add custom models or adjust parameters in `.intellidoc.yml`:

```yaml
openai:
  model: gpt-4-turbo-preview
  temperature: 0.5
  max_tokens: 3000

anthropic:
  model: claude-3-opus-20240229
  temperature: 0.8
  max_tokens: 2500
```

### Programmatic Usage

Use IntelliDoc in your Python code:

```python
from intellidoc.core import (
    MultiModelOrchestrator,
    DocumentationTask,
    ModelConfig,
    ModelProvider,
    CollaborationStrategy
)

# Configure models
configs = [
    ModelConfig(provider=ModelProvider.OPENAI, model_name="gpt-4"),
    ModelConfig(provider=ModelProvider.ANTHROPIC, model_name="claude-3-5-sonnet-20241022")
]

# Create orchestrator
orchestrator = MultiModelOrchestrator(
    configs,
    strategy=CollaborationStrategy.CONSENSUS
)

# Generate documentation
task = DocumentationTask(
    code="def factorial(n): return 1 if n <= 1 else n * factorial(n-1)",
    language="python"
)

result = await orchestrator.generate_documentation(task)
print(result.final_documentation)
print(f"Confidence: {result.confidence_score:.2%}")
```

### Batch Processing

Process multiple files:

```python
import asyncio
from pathlib import Path

async def document_directory(path: str):
    files = Path(path).rglob("*.py")
    tasks = [
        orchestrator.generate_documentation(
            DocumentationTask(code=f.read_text(), language="python")
        )
        for f in files
    ]
    return await asyncio.gather(*tasks)
```

## 🧪 Testing

Run the test suite:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=intellidoc --cov-report=html

# Run only smoke tests
pytest tests/test_smoke.py

# Run integration tests (requires API keys)
pytest -m integration
```

## 🛣️ Roadmap

- [x] **Phase 1**: Core multi-model architecture
- [x] **Phase 2**: CLI and API implementation
- [ ] **Phase 3**: Web UI for documentation management
- [ ] **Phase 4**: Git integration and CI/CD workflows
- [ ] **Phase 5**: Local model support (Llama, CodeLlama)
- [ ] **Phase 6**: Fine-tuning and domain adaptation
- [ ] **Phase 7**: Multi-language AST analysis improvements
- [ ] **Phase 8**: Documentation quality metrics and validation

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Key areas for contribution:
- Adding support for more programming languages
- Implementing new collaboration strategies
- Adding support for additional AI models
- Improving code parsing and analysis
- Writing tests and documentation

## 📖 Research Background

IntelliDoc is inspired by research in multi-agent AI systems and collaborative problem-solving. The multi-model approach is based on the principle that diverse perspectives lead to better solutions - similar to how human teams with complementary expertise outperform individuals.

**Key Concepts**:
- **Ensemble Methods**: Combining multiple models for improved accuracy
- **Consensus Building**: Synthesizing diverse outputs into coherent results
- **Specialization**: Leveraging model-specific strengths
- **Cross-Validation**: Models verify each other's outputs

## 📄 License

IntelliDoc is licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Anthropic for Claude API
- OpenAI for GPT models
- Tree-sitter project for parsing infrastructure
- The open-source community

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/IntelliDoc/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/IntelliDoc/discussions)
- **Email**: your-email@example.com

---

**Made with ❤️ for developers who value great documentation**
