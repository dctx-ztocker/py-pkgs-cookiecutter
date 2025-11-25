# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **fork** of [py-pkgs/py-pkgs-cookiecutter](https://github.com/py-pkgs/py-pkgs-cookiecutter), a cookiecutter template for generating Python packages. This fork extends the original with:

- Clean Architecture / DDD patterns (domain, application, infrastructure layers)
- FastAPI REST API with versioned endpoints
- Docker and docker-compose support
- Automatic setup and dependency installation via cookiecutter hooks
- Makefile with common development commands
- Semantic Release for automated versioning
- Pre-commit hooks for code quality
- CI workflows (GitHub Actions)

## Repository Structure

- **Root level**: The cookiecutter template configuration
- **`{{ cookiecutter.__package_slug }}/`**: The template directory that gets rendered when creating a new project
- **`tests/`**: Tests for the cookiecutter template itself (not the generated package)
- **`docs/`**: Documentation for the cookiecutter template (Sphinx-based)
- **`hooks/`**: Pre- and post-generation hooks for template initialization

## Development Commands

### Setting Up the Cookiecutter Development Environment

```bash
# Install template dependencies
pip install -r requirements.txt

# This installs: cookiecutter >= 2.0.0, pytest
```

### Testing the Cookiecutter Template

```bash
# Run all template tests (parametrized across license/CI combinations)
pytest tests/

# Run a specific test
pytest tests/test_cookiecutter.py::test_cookiecutter_default_options -v

# Generate a test package with default options
cookiecutter . --no-input --output-dir /tmp/test

# Generate a test package with specific options
cookiecutter . --no-input --output-dir /tmp/test \
  package_name="test_pkg" \
  open_source_license="MIT" \
  include_github_actions="ci"
```

### Building Documentation

```bash
cd docs
make html
# Generated docs will be in docs/_build/html
```

## Template Configuration

The template options are defined in `cookiecutter.json`:
- `author_name`: Author name and email
- `package_name`: Name of the generated package
- `package_short_description`: Package description
- `package_version`: Initial version (default: 0.1.0)
- `python_version`: Python version to target (default: 3.12.8)
- `open_source_license`: License choice (MIT, Apache, GPL, BSD, CC0, Proprietary, None)
- `include_github_actions`: CI/CD options (no, ci)

## Generated Package Architecture

The template generates a package following clean architecture/DDD patterns:

```
src/<package>/
├── domain/           # Business logic layer
│   ├── entities/     # Domain entities (Task, TaskList)
│   ├── repositories/ # Repository interfaces
│   └── services/     # Domain services
├── application/      # Use cases/application services
└── infrastructure/   # External concerns
    ├── persistence/  # Database models and repository implementations
    │   ├── models/   # SQLAlchemy models
    │   └── repositories/  # RDS repository implementations
    └── web/          # FastAPI web layer
        ├── api/v1/   # REST API endpoints
        └── ui/       # UI routes
```

### Generated Package Makefile Targets

The generated package includes a Makefile with these commands:

**Development Setup:**
- `make setup` - Setup Python environment (pyenv, Python, virtualenv, Poetry)
- `make deps` - Install dependencies from pyproject.toml
- `make install` - Install package in development mode

**Testing:**
- `make test` - Run unit tests with pytest
- `make test-cov` - Run tests with coverage report

**Running the Application:**
- `make start` - Start FastAPI app (localhost only)
- `make dev-server` - Start FastAPI app (network accessible)
- `make prod-server` - Start FastAPI app in production mode

**Docker:**
- `make docker-build` - Build Docker image
- `make docker-up` - Build and start Docker compose stack
- `make docker-down` - Stop Docker compose stack
- `make docker-logs` - Tail Docker logs

**Utilities:**
- `make clean` - Clean build artifacts
- `make help` - Show available commands

## Cookiecutter Hooks

### Pre-Generation Hook (`hooks/pre_gen_project.py`)

Validates that cookiecutter >= 2.0.0 is installed. Exits with error message if requirement not met.

### Post-Generation Hook (`hooks/post_gen_project.py`)

Runs after template generation to:
1. **Setup Environment**: Runs `make setup` to initialize Python environment (pyenv, virtualenv, Poetry)
2. **Initialize Git**: Creates git repository and makes initial commit with all generated files
3. **Install Dependencies** (Optional): Prompts user to select dependency groups (core, test, linting) and installs them with `poetry add`
4. **Open in VS Code** (Optional): If VS Code is installed, offers to open the project in the editor
5. **Ready to Code**: Displays next steps and available commands

The hook automatically configures git with the author information from the template.

**Interactive Prompts:**
- Dependency groups selection (core, test, linting) - defaults to Yes, can skip with no
- VS Code opening - defaults to Yes, can skip with no
- Only shows in interactive mode (terminals, not CI/CD)

## Generated Package Features

Each generated project includes:

**Clean Architecture Structure:**
- Domain layer (entities, repositories, services)
- Application layer (use cases)
- Infrastructure layer (persistence, web, DI)

**FastAPI REST API:**
- Versioned endpoints (v1)
- Pydantic schemas for validation
- Dependency injection with dependency-injector
- OpenAPI/Swagger documentation at `/docs`

**Database Support:**
- SQLAlchemy ORM
- Alembic migrations
- Support for SQLite (default) and PostgreSQL

**Testing:**
- pytest with fixtures (conftest.py)
- CRUD flow tests
- API integration tests
- Repository tests

**Development Tools:**
- Makefile with 20+ commands
- Pre-commit hooks (ruff, black, mypy, bandit)
- Docker and docker-compose support
- Semantic Release for versioning

## Dependency Groups

The post-generation hook prompts users to optionally install dependency groups:

**Core Dependencies** - Production dependencies:
- FastAPI, SQLAlchemy, Pydantic, Click, Python-dotenv
- Database support: Alembic, databases, aiosqlite, psycopg
- Development tools: pre-commit, semantic-release, ipython, ipdb, twine

**Test Dependencies** - Testing and QA:
- pytest, pytest-cov, pytest-asyncio, coverage, pytest-html, tox, httpx

**Linting Dependencies** - Code quality:
- ruff, black

Users can select any combination of these groups during project generation, and they will be automatically installed using `poetry add`.

## VS Code Configuration

The generated project includes VS Code settings for optimal development experience:

- **Python Interpreter**: Automatically detected from pyenv environment
- **Terminal Integration**: Shells configured to activate the pyenv environment with login shell (`-l` flag)
- **Pytest Integration**: Configured for running tests directly from VS Code
- **Type Checking**: Set to "basic" mode for Python analysis

The `.vscode/settings.json` file includes:
- `python.venvPath`: Points to `~/.pyenv/versions/{python_version}/envs` where pyenv creates virtual environments
- `python.terminal.activateEnvironment`: Disabled (pyenv handles activation via `.python-version`)
- Task automation: Set to manual/on-demand execution

**How VS Code detects the Python environment:**
1. `.python-version` file tells pyenv which environment to activate (e.g., "myproject")
2. `python.venvPath` tells VS Code where to look for venvs (pyenv's envs folder)
3. VS Code matches the project name with the venv name to detect the correct interpreter
4. Terminal automatically uses login shell which activates pyenv

## Key Files

- `cookiecutter.json`: Template variables and available options
- `tests/test_cookiecutter.py`: Parametrized tests covering all license/CI combinations
- `hooks/post_gen_project.py`: Post-generation hook for setup, git init, and optional dependency installation
- `{{ cookiecutter.__package_slug }}/pyproject.toml`: Poetry configuration with semantic-release setup
- `{{ cookiecutter.__package_slug }}/Makefile`: Generated package's development commands
- `{{ cookiecutter.__package_slug }}/scripts/setup_env.sh`: Environment setup script (pyenv, Python, virtualenv, Poetry)
- `{{ cookiecutter.__package_slug }}/.python-version`: Python version specification for pyenv
- `{{ cookiecutter.__package_slug }}/.pre-commit-config.yaml`: Pre-commit hooks configuration
- `{{ cookiecutter.__package_slug }}/.vscode/settings.json`: VS Code configuration for Python development
