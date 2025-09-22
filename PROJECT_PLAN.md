## Project Overview

IntelliDoc is an open‑source tool that leverages artificial intelligence to automatically generate and update code documentation based on changes in a repository.  The project comprises several major components: a FastAPI backend for analysing code and generating documentation, a CLI for developers to interact with the system, a React‑based web front‑end for reviewing and managing documentation, and scripts to support automation and workflow integration.

## High‑Level Phases

### Phase 1: Foundational Setup (Completed)

- Established the repository structure with directories for the API, CLI, scripts, web front‑end and GitHub workflows.
- Added an Apache 2.0 license, a comprehensive Python `.gitignore`, a detailed README and an initial CI workflow to run tests.

### Phase 2: Documentation & CLI/Scripting (Current)

- Implement an automated documentation generation workflow (`docgen.yml`) triggered on pushes to `main`.
- Add a project plan document (this file) outlining development phases and milestones.
- Flesh out the CLI with a Typer‑based interface and create scripts for processing documents.

### Phase 3: Core API Development

- Build the FastAPI backend, integrating Hugging Face Transformer models for natural‑language generation.
- Implement endpoints for submitting code or documents and retrieving generated documentation.
- Introduce asynchronous processing and performance optimisations.

### Phase 4: Web Front‑end Development

- Develop a React/TypeScript user interface for uploading code, reviewing generated documentation and managing projects.
- Incorporate features like dashboards, dark mode and user onboarding to enhance the user experience.

### Phase 5: Deployment & Operationalisation

- Finalise deployment workflows using GitHub Actions, Docker and optional SaaS hosting.
- Implement observability (metrics, logs, tracing) and ensure data privacy and security.

## Key Milestones

- **MVP release:** CLI generates documentation for Python and JavaScript repositories and commits results back to the repository.
- **Beta release:** Web UI available for reviewing and editing generated docs; support for multiple programming languages.
- **Release Candidate:** Full API with authentication, settings and model fine‑tuning; robust documentation site.

## Communication Plan

- Use GitHub Projects to manage tasks and milestones, with issues and PRs for tracking progress.
- Maintain clear documentation in the README and `/docs` directory, including getting started guides and API references.
- Provide periodic updates through release notes and discussions to keep contributors and stakeholders informed.
