# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this project.

## Project Overview

**{{ cookiecutter.package_name }}** is a REST API project built with FastAPI implementing Clean Architecture / Domain-Driven Design (DDD) patterns.

**Status**: This is a basic example template. Features, endpoints, and business logic should be expanded and customized for your specific use case.

## Project Structure

The project follows Clean Architecture with three main layers:

```
src/{{ cookiecutter.__package_slug }}/
├── domain/                 # Business logic (entities, repositories interfaces, services)
│   ├── entities/          # Domain models (e.g., Task, TaskList)
│   ├── repositories/      # Repository interfaces (contracts)
│   ├── services/          # Domain services (business rules)
│   └── shared/            # Shared domain types/exceptions
├── application/           # Use cases and application services
├── infrastructure/        # External integrations (database, web, DI)
│   ├── persistence/       # Database models and repository implementations
│   │   ├── models/       # SQLAlchemy ORM models
│   │   └── repositories/ # Repository implementations
│   └── web/              # FastAPI web layer
│       ├── api/v1/       # REST API endpoints (v1)
│       │   └── schemas/  # Pydantic request/response schemas
│       └── dependencies/ # FastAPI dependency injection
└── {{ cookiecutter.__package_slug }}.py  # FastAPI app factory
```

## File Organization

- **`__init__.py` files are intentionally blank** - Explicit imports prevent circular dependencies
- **All imports must be explicit** - Use full paths from the package root
- **Type hints are required** - All functions should have type annotations
- **Pydantic models for validation** - Request/response schemas in `infrastructure/web/api/v1/schemas/`

## Development Commands

### Environment Setup

```bash
# The environment is automatically set up during project generation
# If you need to re-run setup:
make setup

# Install/update dependencies:
make deps
```

### Testing

```bash
# Run all tests
make test

# Run tests with coverage report
make test-cov

# Run only infrastructure tests (database, API)
poetry run pytest tests/{{ cookiecutter.__package_slug }}/infrastructure/ -v

# Run only API tests
poetry run pytest tests/{{ cookiecutter.__package_slug }}/infrastructure/web/ -v
```

### Running the Application

```bash
# Start FastAPI in development mode (localhost only)
make start

# Start FastAPI accessible from other devices
make dev-server

# Start FastAPI in production mode
make prod-server

# API documentation will be available at:
# - Swagger UI: http://localhost:8000/docs
# - ReDoc: http://localhost:8000/redoc
```

### Testing the API

```bash
# Run complete CRUD flow tests (requires app running with 'make start')
make test-crud

# Run API tests (requires app running)
make test-api

# Run API tests with verbose output
make test-api-verbose
```

## Code Style and Conventions

### Imports
- Use explicit imports: `from {{ cookiecutter.__package_slug }}.domain.entities import Task`
- Avoid wildcard imports: ❌ `from module import *`
- Group imports: stdlib → third-party → local

### Type Hints
- All function parameters must have type hints
- All return types must be specified
- Use `Optional[T]` for nullable values: `def get_task(id: int) -> Optional[Task]:`

### Naming
- **Classes**: PascalCase (`Task`, `TaskRepository`)
- **Functions/methods**: snake_case (`create_task`, `get_by_id`)
- **Constants**: UPPER_SNAKE_CASE (`MAX_RETRIES`, `DEFAULT_TIMEOUT`)
- **Private methods**: prefix with underscore (`_validate_input`)

### Example Function

```python
from typing import Optional
from {{ cookiecutter.__package_slug }}.domain.entities import Task

def create_task(title: str, description: Optional[str] = None) -> Task:
    """Create a new task with validation.

    Args:
        title: Task title (required)
        description: Optional task description

    Returns:
        The created Task instance

    Raises:
        ValueError: If title is empty
    """
    if not title.strip():
        raise ValueError("Title cannot be empty")

    return Task(title=title, description=description)
```

## Architecture Layers Explained

### Domain Layer (`domain/`)
- **Entities**: Core business models (Task, TaskList)
- **Repositories**: Interfaces defining data access contracts
- **Services**: Business logic that doesn't fit in entities
- **Dependencies**: Domain layer imports nothing else from the application

### Application Layer (`application/`)
- **Use Cases**: Orchestrate domain entities and repositories
- **Application Services**: Coordinate business operations
- **Dependencies**: Only imports from domain layer

### Infrastructure Layer (`infrastructure/`)
- **Persistence**: Database models, ORM mappings, repository implementations
- **Web**: FastAPI routes, schemas, dependency injection
- **Dependencies**: Can import from domain and application

## Testing Strategy

### Test Organization
```
tests/{{ cookiecutter.__package_slug }}/
├── infrastructure/
│   ├── persistence/repositories/
│   │   ├── test_task_repository_rds.py
│   │   └── test_task_list_repository_rds.py
│   └── web/
│       └── test_api.py
```

### Running Tests
1. **Unit tests**: `make test`
2. **With coverage**: `make test-cov`
3. **Specific test file**: `poetry run pytest tests/{{ cookiecutter.__package_slug }}/infrastructure/web/test_api.py -v`
4. **Specific test**: `poetry run pytest tests/{{ cookiecutter.__package_slug }}/infrastructure/web/test_api.py::test_create_task -v`

### Writing Tests
- Use pytest fixtures for common setup
- Mock external dependencies (database, external APIs)
- Test both success and error paths
- Keep tests focused and readable

## Database

The project uses **SQLAlchemy** with **SQLite** by default (can be switched to PostgreSQL).

### Running Migrations
```bash
# Create initial migration
poetry run alembic revision --autogenerate -m "Initial migration"

# Apply migrations
poetry run alembic upgrade head

# Rollback last migration
poetry run alembic downgrade -1
```

## Pre-commit Hooks

The project includes pre-commit hooks for code quality:

```bash
# Install hooks
pre-commit install

# Run manually on all files
pre-commit run --all-files

# Bypass hooks (not recommended)
git commit --no-verify
```

## Key Files

- **`pyproject.toml`**: Project metadata and dependencies
- **`.python-version`**: Python version for pyenv
- **`Makefile`**: Common development commands
- **`scripts/setup_env.sh`**: Environment initialization script
- **`.vscode/settings.json`**: VS Code configuration (Python interpreter, testing)
- **`.pre-commit-config.yaml`**: Pre-commit hooks configuration

## Customizing the Project

This template provides a basic REST API structure. To customize:

1. **Add domain entities**: Create new files in `src/{{ cookiecutter.__package_slug }}/domain/entities/`
2. **Add repositories**: Define interfaces in `domain/repositories/` and implementations in `infrastructure/persistence/repositories/`
3. **Add use cases**: Create application services in `application/`
4. **Add API endpoints**: Create routes in `infrastructure/web/api/v1/`
5. **Add database models**: SQLAlchemy models in `infrastructure/persistence/models/`
6. **Add tests**: Follow the existing test structure

## Common Tasks with Claude

### Ask Claude to explain the codebase
```
"Explain the architecture of this project and how the three layers interact"
```

### Ask Claude to add a new feature
```
"Add a new endpoint to list all tasks with pagination. Follow the existing architecture pattern."
```

### Ask Claude to fix a bug
```
"The task creation is failing with a validation error. Debug and fix the issue."
```

### Ask Claude to add tests
```
"Add comprehensive tests for the task repository, including edge cases."
```

### Ask Claude to refactor code
```
"Refactor the task service to improve readability and follow SOLID principles."
```

## Useful Commands Reference

| Command | Purpose |
|---------|---------|
| `make help` | Show all available commands |
| `make setup` | Setup Python environment |
| `make deps` | Install dependencies |
| `make test` | Run tests |
| `make test-cov` | Tests with coverage |
| `make start` | Start development server |
| `make clean` | Clean build artifacts |
| `make docker-build` | Build Docker image |
| `make docker-up` | Start Docker services |

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLAlchemy ORM**: https://docs.sqlalchemy.org/
- **Pydantic**: https://docs.pydantic.dev/
- **pytest**: https://docs.pytest.org/
- **Clean Architecture**: https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html
- **Domain-Driven Design**: https://martinfowler.com/bliki/DomainDrivenDesign.html
