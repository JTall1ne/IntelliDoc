# IntelliDoc

IntelliDoc is an open-source tool that uses artificial intelligence to automatically generate and update code documentation based on changes in your repository. It analyses commit diffs, understands the structure of your code and produces human-friendly documentation that stays in sync with your source.

## Features

- **Automated documentation generation** – Runs on each commit to produce or update README and API docs for supported languages.
- **Multi-language support** – Works with popular programming languages like Python, JavaScript and Java.
- **CI/CD integration** – Ready to run via GitHub Actions or other pipelines to enforce up-to-date documentation on every push.
- **Web-based review interface** – Provides a simple UI to preview and edit generated documentation before publishing.
- **Open-core architecture** – The core is open source and free; advanced features will be available via an optional hosted version.

## Getting  Started

IntelliDoc is now production-ready and can be installed via pip or from source.

### Install via pip

```bash
pip install intellidoc
```

### Install from source

```bash
git clone https://github.com/JTall1ne/IntelliDoc.git
cd IntelliDoc
pip install -e .
```

### Configure environment variables

Copy `.env.template` to `.env` and provide your API keys:

```bash
cp .env.template .env
# Then edit .env to add your keys
OPENAI_API_KEY=your-openai-api-key
GITHUB_TOKEN=your-github-token
```

### Run the CLI

Generate documentation for a repository:

```bash
intellidoc path/to/your/repository
```

This will analyze your code and update README files and API documentation accordingly.

## Contributing

1. Fork this repository and clone your fork locally.
2. Set up a Python virtual environment and install dependencies (`pip install -e .`).
3. Create a branch for your feature or fix and submit a pull request.


## Roadmap

See the upcoming `PROJECT_PLAN.md` (to be added) for a high-level project plan covering MVP, Beta, Release Candidate and SaaS phases.

## License

IntelliDoc is licensed under the Apache License, Version 2.0. See the [LICENSE](LICENSE) file for details.
