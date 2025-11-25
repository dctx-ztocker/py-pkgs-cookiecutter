.PHONY: help setup deps docker docker-up docker-down docker-logs test test-cov clean install start dev prod test-crud test-api test-api-verbose

# Default target
help:
	@echo "Available commands:"
	@echo ""
	@echo "🚀 Application Commands:"
	@echo "  start         - Start FastAPI app (localhost only)"
	@echo "  dev-server    - Start FastAPI app in dev mode (accessible from network)"
	@echo "  prod-server   - Start FastAPI app in production mode"
	@echo ""
	@echo "🔧 Development Commands:"
	@echo "  setup         - Setup Python development environment"
	@echo "  deps          - Install dependencies from pyproject.toml"
	@echo "  install       - Install package in development mode"
	@echo "  test          - Run unit tests with pytest"
	@echo "  test-cov      - Run tests with coverage report"
	@echo "  test-api      - Run API CRUD tests"
	@echo "  test-api-verbose - Run API tests with verbose output"
	@echo "  clean         - Clean build artifacts"
	@echo ""
	@echo "🐳 Docker Commands:"
	@echo "  docker-build  - Build Docker image"
	@echo "  docker-up     - Build and start compose stack (.build/docker-compose.yml)"
	@echo "  docker-down   - Stop and remove compose stack"
	@echo "  docker-logs   - Tail logs from compose stack"
	@echo ""
	@echo "📚 Other Commands:"
	@echo "  help          - Show this help message"
	@echo "  dev           - Quick development workflow (setup + install + test)"
	@echo "  full-setup    - Full setup including dependencies"

# Setup Python development environment
setup:
	@echo "🔧 Setting up Python development environment..."
	@bash -c "./scripts/setup_env.sh"

# Install dependencies from pyproject.toml
deps:
	@echo "📦 Installing dependencies..."
	poetry install

# Build Docker image
docker-build:
	@echo "🐳 Building Docker image..."
	@bash -c "./scripts/build_docker.sh"

# Docker Compose helpers (keep Docker files under .build/)
docker-up: docker-down
	@echo "🐳 Building and starting docker-compose stack..."
	@bash -c "docker compose -f .build/docker-compose.yml up --build $(ARGS)"


docker-down:
	@echo "🛑 Stopping docker-compose stack..."
	@bash -c "docker compose -f .build/docker-compose.yml down"

docker-logs:
	@echo "📜 Tailing docker-compose logs... (Ctrl+C to stop)"
	@bash -c "docker compose -f .build/docker-compose.yml logs -f"

# Run unit tests
test:
	@echo "🧪 Running unit tests..."
	@echo "📁 Test directory: $(PWD)/tests/"
	@echo "🔍 Verbose output enabled"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run pytest tests/ -v
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ Unit tests completed!"

# Run tests with coverage
test-cov:
	@echo "🧪 Running tests with coverage..."
	@echo "📁 Test directory: $(PWD)/tests/"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run pytest tests/ --cov=src/{{ cookiecutter.__package_slug }} --cov-report=term-missing
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ Coverage tests completed!"


# Install package in development mode
install:
	@echo "📦 Installing package in development mode..."
	poetry install

# Clean build artifacts
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleanup completed!"

# Quick development workflow
dev: setup install test
	@echo "✅ Development environment ready!"

# Full setup including dependencies
full-setup: setup install
	@echo "✅ Full setup completed!"

# Start the FastAPI application
start:
	@echo "🚀 Starting FastAPI application..."
	@echo "📖 API Documentation: http://127.0.0.1:8000/docs"
	@echo "🔍 ReDoc: http://127.0.0.1:8000/redoc"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run uvicorn {{ cookiecutter.__package_slug }}.{{ cookiecutter.__package_slug }}:app --reload --host 127.0.0.1 --port 8000

# Start in development mode (accessible from other devices)
dev-server:
	@echo "🌐 Starting FastAPI application in development mode..."
	@echo "📖 API Documentation: http://0.0.0.0:8000/docs"
	@echo "🔍 ReDoc: http://0.0.0.0:8000/redoc"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run uvicorn {{ cookiecutter.__package_slug }}.{{ cookiecutter.__package_slug }}:app --reload --host 0.0.0.0 --port 8000

# Start in production mode
prod-server:
	@echo "🚀 Starting FastAPI application in production mode..."
	@echo "📖 API Documentation: http://0.0.0.0:8000/docs"
	@echo "🔍 ReDoc: http://0.0.0.0:8000/redoc"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run uvicorn {{ cookiecutter.__package_slug }}.{{ cookiecutter.__package_slug }}:app --host 0.0.0.0 --port 8000

# Run CRUD flow tests
test-crud:
	@echo "🧪 Running complete CRUD flow tests..."
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run python scripts/test_crud_flow.py
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ CRUD flow tests completed!"

# Run API CRUD tests
test-api:
	@echo "🧪 Running complete API CRUD tests..."
	@echo "⚠️  Make sure the API is running with 'make start' in another terminal"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run python scripts/test_api_full_crud.py
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ API CRUD tests completed!"

# Run API CRUD tests with verbose output
test-api-verbose:
	@echo "🧪 Running complete API CRUD tests (verbose)..."
	@echo "⚠️  Make sure the API is running with 'make start' in another terminal"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	poetry run python scripts/test_api_full_crud.py --verbose
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "✅ API CRUD tests completed!"
