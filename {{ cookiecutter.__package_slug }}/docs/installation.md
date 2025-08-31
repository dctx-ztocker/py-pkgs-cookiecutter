# Installation Guide

## Overview

This project supports multiple installation methods:

1. **Automatic (VS Code/Cursor)**: Environment setup happens automatically when opening the project
2. **Script-based**: Using the provided setup script
3. **Manual**: Step-by-step manual installation

## Prerequisites

- [pyenv installed](https://github.com/pyenv/pyenv#installation)
- [pyenv-virtualenv plugin installed](https://github.com/pyenv/pyenv-virtualenv#installation)

## Method 1: Automatic Setup (VS Code/Cursor)

### VS Code Setup Steps

1. **Open the project in VS Code**
   - The project will automatically run the setup script
   - A notification will appear showing the setup progress

2. **Verify the setup**
   - Check the bottom-left corner for the Python interpreter
   - It should display `{{ cookiecutter.__package_slug }}` as the active environment
   - The integrated terminal will automatically use the correct environment

3. **Start coding**
   - Your environment is ready to use
   - All dependencies will be automatically installed

## Method 2: Script-based Setup

### Script Execution Steps

1. **Run the setup script**

   ```bash
   ./scripts/setup_env.sh
   ```

2. **For verbose output**

   ```bash
   ./scripts/setup_env.sh --verbose
   ```

3. **For quiet mode**

   ```bash
   ./scripts/setup_env.sh --quiet
   ```

The script will:

- Check if pyenv and pyenv-virtualenv are available
- Verify Python {{ cookiecutter.python_version }} is installed
- Create a virtual environment named `{{ cookiecutter.__package_slug }}`
- Install Poetry 2.1.3
- Configure the local Python version

## Method 3: Manual Setup

### Manual Setup Steps

#### 1. Virtual Environment Setup

First, remove any previous installation:

```bash
pyenv virtualenv-delete -f {{ cookiecutter.__package_slug }}
rm .python-version
pyenv uninstall -f {{ cookiecutter.python_version }}
```

Then, create and set up the new virtual environment:

```bash
pyenv install {{ cookiecutter.python_version }} -f
pyenv virtualenv {{ cookiecutter.python_version }} {{ cookiecutter.__package_slug }}
pyenv local {{ cookiecutter.__package_slug }}
pip install --upgrade pip
pip install poetry==2.1.3
```

#### 2. Dependencies Installation

Configure Poetry and install dependencies:

```bash
poetry config virtualenvs.create true
poetry install
```

Set up development tools:

```bash
# Install pre-commit hooks
poetry run pre-commit install

# Get virtual environment path for IDEs
poetry env info -e | pbcopy
```

## VS Code Configuration

The project includes pre-configured VS Code settings:

### Automatic Tasks

- **Setup Python Env (auto)**: Runs automatically when opening the project
- **Terminal Profile**: Automatically activates the environment in new terminals

### Settings

- Python interpreter path is automatically configured
- Virtual environment activation is enabled
- Type checking is set to basic mode

### Manual Task Execution

If you need to run the setup manually:

1. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
2. Type "Tasks: Run Task"
3. Select "Setup Python Env (auto)"

## Troubleshooting

### Common Issues

1. **pyenv not found**

   ```bash
   # Install pyenv (macOS)
   brew install pyenv pyenv-virtualenv

   # Add to your shell profile
   echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
   echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
   echo 'eval "$(pyenv init -)"' >> ~/.zshrc
   ```

2. **Virtual environment not activating**

   ```bash
   # Check current pyenv version
   pyenv version

   # Set local version
   pyenv local {{ cookiecutter.__package_slug }}
   ```

3. **Poetry installation fails**

   ```bash
   # Upgrade pip first
   pip install --upgrade pip

   # Install poetry with specific version
   pip install poetry==2.1.3
   ```

## Verification

After completing any installation method, verify your setup with these commands:

```bash
# Verify Python version
python --version

# Verify pyenv environment
pyenv version

# Verify Poetry
poetry --version

# Check installed packages
poetry show

# Verify environment activation
pyenv shell {{ cookiecutter.__package_slug }}
```

**Expected output for successful setup:**

- Python version should show {{ cookiecutter.python_version }}
- pyenv version should show `{{ cookiecutter.__package_slug }}`
- Poetry version should show 2.1.3
- Environment should activate without errors

## Environment Details

- **Python Version**: {{ cookiecutter.python_version }}
- **Package Manager**: Poetry 2.1.3
- **Virtual Environment**: {{ cookiecutter.__package_slug }} (managed by pyenv)
- **Development Tools**: pre-commit, pytest
