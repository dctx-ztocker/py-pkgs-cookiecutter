# Repository usage

This guide covers day-to-day usage of the project: commands, workflow, and best practices.

Note: for installation and environment setup, see [`docs/installation.md`](installation.md).

## Typical workflow

1. Create or edit code in `src/{{ cookiecutter.__package_slug }}/`
2. Add or update tests in `tests/`
3. Run linters and formatters
4. Run tests and coverage
5. Commit using Conventional Commits

## Key commands (Makefile)

- `make test`: run tests (`pytest -v`)
- `make test-cov`: run tests with coverage (`--cov={{ cookiecutter.__package_slug }}`)
- `make deps`, `make deps-core`, `make deps-test`: manage base dependencies via scripts
- `make docker`: build the Docker image
- `make clean`: remove build artifacts and caches

## Dependency management

- Important: always add or remove dependencies using Poetry commands. Do not edit `pyproject.toml` by hand; Poetry will
  update it for you.

- Helper script:

```bash
./scripts/add_deps.sh --core   # runtime and essential dev dependencies
./scripts/add_deps.sh --test   # testing tools
./scripts/add_deps.sh --all    # everything above
```

- Directly with Poetry:

```bash
poetry add <package>
poetry add --group dev <dev_package>
```

## Development and testing

- Unit tests:

```bash
make test
```

- With coverage:

```bash
make test-cov
```

- Matrix/isolated via tox:

```bash
poetry run tox
```

## Code quality

Configured hooks: `ruff`, `black`, `markdownlint`, `mypy`, `bandit`, `detect-secrets`, `interrogate`.

Run all hooks manually:

```bash
poetry run pre-commit run -a
```

## Package usage

Minimal example (current API):

```python
import {{ cookiecutter.__package_slug }}

print({{ cookiecutter.__package_slug }}.__version__)
```

Tip: export public functions/classes from `src/{{ cookiecutter.__package_slug }}/__init__.py` for a clean API and add tests in `tests/{{ cookiecutter.__package_slug }}/`.

## Versioning and releases

- Versioning managed by `python-semantic-release` (configured in `pyproject.toml`)
- Use Conventional Commits: `feat: ...`, `fix: ...`, `chore: ...`, etc.

Manual publish (if applicable):

```bash
poetry build
poetry publish
```

For automated pipelines, configure required tokens in your CI.

## Docker

Build the image:

```bash
make docker
```

Print package version with Docker Compose (files under `.build/`):

```bash
make docker-up   # builds if needed and runs compose
make docker-logs # show output
make docker-down # stop and clean
```

## Next steps

- Implement features in `src/{{ cookiecutter.__package_slug }}/` and test them in `tests/`
- Document the API under `docs/`
