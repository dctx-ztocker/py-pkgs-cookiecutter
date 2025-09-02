#!/bin/bash

# Minimalist script to add Poetry dependencies
# Usage: ./add_deps.sh [--core] [--test] [--all]

# Set timeout for poetry commands (in seconds)
POETRY_TIMEOUT=300  # 5 minutes

# Ensure we're in the right directory and environment
setup_environment() {
    echo "Setting up environment..."

    # Change to script directory if needed
    cd "$(dirname "$0")/.." || exit 1

    # Check if we're in a Poetry project
    if [[ ! -f "pyproject.toml" ]]; then
        echo "Error: pyproject.toml not found in current directory"
        exit 1
    fi

    # Try to activate pyenv environment if available
    if command -v pyenv &> /dev/null; then
        echo "Activating pyenv environment..."
        eval "$(pyenv init -)"
        if [[ -f ".python-version" ]]; then
            local python_version=$(cat .python-version)
            echo "Using Python version: $python_version"
            pyenv shell "$python_version"
        fi
    fi

    # Check if Poetry is available
    if ! command -v poetry &> /dev/null; then
        echo "Error: Poetry not found in PATH"
        echo "Current PATH: $PATH"
        exit 1
    fi

    echo "Poetry version: $(poetry --version)"
    echo "Python version: $(python --version)"
    echo "Environment setup completed."
}

# Function to run poetry add with timeout
poetry_add_with_timeout() {
    local timeout_cmd="timeout $POETRY_TIMEOUT"
    if ! command -v timeout &> /dev/null; then
        timeout_cmd=""  # No timeout if timeout command not available
    fi

    echo "Running: poetry $*"
    if [ -n "$timeout_cmd" ]; then
        $timeout_cmd poetry "$@"
    else
        poetry "$@"
    fi

    local exit_code=$?
    if [ $exit_code -eq 124 ]; then
        echo "Error: Command timed out after ${POETRY_TIMEOUT} seconds"
        return 1
    elif [ $exit_code -ne 0 ]; then
        echo "Error: poetry command failed with exit code $exit_code"
        return 1
    fi
    echo "Command completed successfully."
    return 0
}

show_help() {
    echo "Usage: $0 [OPTIONS]"
    echo "  --core         Install core dependencies"
    echo "  --test         Install testing tools"
    echo "  --linting      Install linting and formatting tools"
    echo "  --all          Install everything (default behavior)"
    echo "  --help         Show this help"
    echo "No options: Install all dependencies automatically"
}

# =============================================================================
# CORE DEPENDENCIES SECTION
# =============================================================================
# Add new core dependencies here:
# - For runtime dependencies: Add to install_core() function
# - For development dependencies: Add to install_core() function with --group dev flag
# - Update pyproject.toml accordingly
# =============================================================================

install_core() {
    local publish="$1"
    if [ "$publish" = "true" ]; then
        echo "Installing complete core dependencies..."

        # Runtime dependencies (required for package to work)
        poetry_add_with_timeout add "click^8.2.1" python-dotenv pydantic || return 1
        poetry_add_with_timeout add pydantic-settings email-validator || return 1
        poetry_add_with_timeout add sqlalchemy fastapi uvicorn || return 1
        poetry_add_with_timeout add alembic dependency-injector || return 1
        poetry_add_with_timeout add databases aiosqlite python-multipart || return 1
        poetry_add_with_timeout add greenlet requests psycopg[binary] || return 1

        # Development dependencies (for publishing and development)
        poetry_add_with_timeout add --group dev twine pre-commit || return 1
        poetry_add_with_timeout add --group dev "python-semantic-release^9.21.1" || return 1
        poetry_add_with_timeout add --group dev ipython ipdb || return 1

        # TODO: Add new runtime dependencies here:
        # poetry_add_with_timeout add package-name || return 1

        # TODO: Add new development dependencies here:
        # poetry_add_with_timeout add --group dev package-name || return 1

    else
        echo "Installing basic core dependencies..."

        # Basic runtime dependencies only
        poetry_add_with_timeout add "click^8.2.1" python-dotenv pydantic || return 1

        # TODO: Add new basic runtime dependencies here:
        # poetry_add_with_timeout add package-name || return 1
    fi
}

# =============================================================================
# TESTING DEPENDENCIES SECTION
# =============================================================================
# Add new testing dependencies here:
# - Update install_test() function
# - Update pyproject.toml accordingly
# - Consider if the dependency should be in dev group or test group
# =============================================================================

install_test() {
    echo "Installing testing tools..."

    # Core testing framework
    poetry_add_with_timeout add --group dev pytest pytest-cov pytest-asyncio || return 1

    # Test coverage and reporting tools
    poetry_add_with_timeout add --group dev coverage[toml] pytest-cov || return 1

    # Additional testing tools
    poetry_add_with_timeout add --group dev pytest-html || return 1

    # Tox for test automation and multi-environment testing
    poetry_add_with_timeout add --group dev tox || return 1

    # HTTP client for testing
    poetry_add_with_timeout add --group dev httpx || return 1

    # TODO: Add new testing dependencies here:
    # poetry_add_with_timeout add --group dev package-name || return 1

    # TODO: Add specialized testing tools here:
    # - Mocking: pytest-mock, unittest.mock
    # - Parameterized tests: pytest-parametrize
    # - Performance testing: pytest-benchmark
    # - Property-based testing: hypothesis
    # - API testing: pytest-httpx, requests-mock
}

# =============================================================================
# ADDITIONAL DEPENDENCY GROUPS SECTION
# =============================================================================
# Add new dependency groups here:
# - Create new functions for specialized dependency groups
# - Examples: linting, documentation, security, performance, etc.
# =============================================================================

install_linting() {
    echo "Installing linting and formatting tools..."
    poetry_add_with_timeout add --group dev ruff black || return 1
}

# TODO: Add new dependency group functions here:
# install_docs() {
#     echo "Installing documentation tools..."
#     poetry_add_with_timeout add --group docs sphinx sphinx-rtd-theme || return 1
# }
#
# install_security() {
#     echo "Installing security tools..."
#     poetry_add_with_timeout add --group dev bandit safety || return 1
# }

main() {
    setup_environment

    # If no arguments, install all by default (non-interactive)
    if [ $# -eq 0 ]; then
        echo "Installing all dependencies by default..."
        if install_core "true" && install_test && install_linting; then
            echo "Installation completed successfully."
            exit 0
        else
            echo "Installation failed."
            exit 1
        fi
    fi

    # Process flags
    local success=true
    while [[ $# -gt 0 ]]; do
        case $1 in
            --core)
                if ! install_core "true"; then
                    success=false
                fi
                ;;
            --test)
                if ! install_test; then
                    success=false
                fi
                ;;
            --linting)
                if ! install_linting; then
                    success=false
                fi
                ;;
            --all)
                if ! install_core "true" || ! install_test || ! install_linting; then
                    success=false
                fi
                ;;
            --help|-h)
                show_help
                exit 0
                ;;
            *)
                echo "Error: Unknown option '$1'"
                show_help
                exit 1
                ;;
        esac
        shift
    done

    if [ "$success" = true ]; then
        echo "Installation completed successfully."
        exit 0
    else
        echo "Installation completed with errors."
        exit 1
    fi
}

main "$@"
