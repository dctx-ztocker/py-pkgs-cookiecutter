#!/usr/bin/env python
"""
Post-generation hook for cookiecutter template.

This hook:
1. Sets up the Python environment (pyenv, virtualenv, Poetry)
2. Initializes git repository
3. Asks user which dependencies to install and installs them
"""

import subprocess
import sys
import os


# Available dependency groups with their packages
DEPENDENCY_GROUPS = [
    {
        "name": "core",
        "description": "Core dependencies (FastAPI, SQLAlchemy, etc.)",
        "packages": [
            "click^8.2.1",
            "python-dotenv",
            "pydantic",
            "pydantic-settings",
            "email-validator",
            "sqlalchemy",
            "fastapi",
            "uvicorn",
            "alembic",
            "dependency-injector",
            "databases",
            "aiosqlite",
            "python-multipart",
            "greenlet",
            "requests",
            "psycopg[binary]",
        ],
        "dev_packages": [
            "twine",
            "pre-commit",
            "python-semantic-release^9.21.1",
            "ipython",
            "ipdb",
        ],
    },
    {
        "name": "test",
        "description": "Testing tools (pytest, pytest-cov, etc.)",
        "packages": [],
        "dev_packages": [
            "pytest",
            "pytest-cov",
            "pytest-asyncio",
            "coverage[toml]",
            "pytest-html",
            "tox",
            "httpx",
        ],
    },
    {
        "name": "linting",
        "description": "Linting & formatting (ruff, black, etc.)",
        "packages": [],
        "dev_packages": [
            "ruff",
            "black",
        ],
    },
]


def run_command(cmd, description, verbose=False):
    """Run a shell command and handle errors."""
    if verbose:
        print(f"\n▶ {description}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=not verbose,
            text=True
        )
        return True
    except subprocess.CalledProcessError as e:
        if verbose:
            print(f"✗ Error during {description}")
        return False


def is_interactive():
    """Check if stdin is available for interactive input."""
    import sys
    return sys.stdin.isatty()


def ask_yes_no(question, default=True):
    """Ask user a yes/no question. Default is yes."""
    while True:
        try:
            default_str = "[Y/n]" if default else "[y/N]"
            response = input(f"{question} {default_str}: ").strip().lower()

            if response == "":
                return default
            elif response in ["y", "yes"]:
                return True
            elif response in ["n", "no"]:
                return False
            else:
                print("⚠ Please enter 'y', 'n', or press Enter for default")
        except EOFError:
            # No stdin available, return default
            return default


def ask_for_dependency_groups():
    """Ask user which dependency groups to install (after setup)."""
    if not is_interactive():
        return []

    print("\n" + "="*60)
    print("📦 OPTIONAL DEPENDENCIES")
    print("="*60)
    print("\nWould you like to install optional dependencies now?")
    print("(You can also run 'make deps' later to install all)")
    print("")

    selected_groups = []

    for group in DEPENDENCY_GROUPS:
        if ask_yes_no(f"  {group['name']:<8} - {group['description']}?"):
            selected_groups.append(group["name"])

    return selected_groups


def get_python_version_from_pyenv():
    """Get the Python version from .python-version file."""
    try:
        with open(".python-version", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def activate_pyenv_and_add_deps(groups):
    """Add dependencies using poetry in the activated pyenv environment."""
    if not groups:
        return True

    # Get the Python version/env name
    env_name = get_python_version_from_pyenv()
    if not env_name:
        print("⚠ Could not determine Python version from .python-version")
        return False

    # Collect all packages to install
    all_packages = []
    all_dev_packages = []

    for group_name in groups:
        group = next((g for g in DEPENDENCY_GROUPS if g["name"] == group_name), None)
        if group:
            all_packages.extend(group["packages"])
            all_dev_packages.extend(group["dev_packages"])

    success = True

    # Get poetry path - use the version from .python-version
    poetry_path = os.path.expanduser(f"~/.pyenv/versions/{env_name}/bin/poetry")

    # Verify poetry exists
    if not os.path.exists(poetry_path):
        # Try to find poetry in current environment
        result = subprocess.run("which poetry", shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            print("⚠ Poetry not found in the environment. Skipping dependency installation.")
            print("You can install dependencies later with: make deps")
            return False
        poetry_path = result.stdout.strip()

    # Build all package strings
    if all_packages:
        print(f"\n▶ Installing runtime dependencies...")
        packages_str = " ".join(all_packages)
        cmd = f'bash -l -c "cd {os.getcwd()} && {poetry_path} add {packages_str}"'
        if not run_command(cmd, "Installing runtime dependencies", verbose=True):
            success = False

    # Install development dependencies
    if all_dev_packages:
        print(f"\n▶ Installing development dependencies...")
        dev_packages_str = " ".join(all_dev_packages)
        cmd = f'bash -l -c "cd {os.getcwd()} && {poetry_path} add --group dev {dev_packages_str}"'
        if not run_command(cmd, "Installing development dependencies", verbose=True):
            success = False

    return success


def install_dependency_groups(groups):
    """Install specified dependency groups using poetry add."""
    if not groups:
        return True

    print(f"\nInstalling: {', '.join(groups)}")
    success = activate_pyenv_and_add_deps(groups)

    if success:
        print("\n✓ Dependencies installed successfully!")
    else:
        print("\n⚠ Some dependencies failed to install.")
        print("You can retry later with: make deps")

    return success


def run_setup():
    """Run the setup process."""
    # Try to use make if available
    if subprocess.run("which make", shell=True, capture_output=True).returncode == 0:
        return run_command("make setup", "Setting up environment", verbose=True)
    else:
        # Fallback: install poetry and run basic setup
        success = True
        success = run_command("pip install poetry", "Installing poetry", verbose=True) and success
        success = run_command("poetry install", "Installing dependencies", verbose=True) and success
        return success


def init_git_repo():
    """Initialize git repository and make initial commit."""
    # Check if git is already initialized
    if subprocess.run("git rev-parse --git-dir", shell=True, capture_output=True).returncode == 0:
        return True  # Already a git repo

    # Initialize git
    if not run_command("git init", "Initializing git repository", verbose=False):
        return False

    # Configure git for this repo (use template author info)
    author_name = "{{ cookiecutter.author_name }}"
    # Extract email if present, otherwise use a default
    if "<" in author_name and ">" in author_name:
        email = author_name[author_name.index("<")+1:author_name.index(">")]
        name = author_name[:author_name.index("<")].strip()
    else:
        name = author_name
        email = "dev@example.com"

    run_command(f'git config user.name "{name}"', "Configuring git name", verbose=False)
    run_command(f'git config user.email "{email}"', "Configuring git email", verbose=False)

    # Stage all files
    if not run_command("git add .", "Staging files", verbose=False):
        return False

    # Make initial commit
    commit_message = "Initial commit: Project setup with template"
    cmd = f'git commit -m "{commit_message}"'
    if not run_command(cmd, "Creating initial commit", verbose=False):
        return False

    return True


def open_in_vscode():
    """Check if VS Code is available and ask user if they want to open the project."""
    # Check if code command exists
    if subprocess.run("which code", shell=True, capture_output=True).returncode != 0:
        return True  # code not available, but that's ok

    if not is_interactive():
        return True  # non-interactive mode, skip

    if ask_yes_no("\n🔧 Open project in VS Code?", default=True):
        try:
            subprocess.Popen(["code", "."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            print(f"⚠ Could not open VS Code: {e}")
            return False

    return True


def main():
    """Main hook function."""
    print("\n" + "="*70)
    print("PROJECT SETUP")
    print("="*70)

    # Step 1: Setup environment (Python, Poetry, venv)
    print("\n[1/3] Setting up environment (pyenv, Python, virtualenv, Poetry)...")
    setup_ok = run_setup()

    if not setup_ok:
        print("\n⚠ Setup had issues. You may need to run 'make setup' manually.")

    # Step 2: Initialize git repository
    print("[2/3] Initializing git repository...")
    init_git_repo()

    # Step 3: Ask for optional dependencies
    print("[3/3] Installing optional dependencies...")
    selected_groups = ask_for_dependency_groups()
    if selected_groups:
        install_dependency_groups(selected_groups)

    # Final message
    print("\n" + "="*70)
    print("✓ READY TO CODE")
    print("="*70)
    print("\nYour environment is configured! Next steps:")
    print("\n  $ cd {{ cookiecutter.__package_slug }}")
    print("  $ make help              # See all available commands")
    print("\nQuick start:")
    print("  $ make test              # Run tests")
    print("  $ make start             # Start FastAPI server")
    print("")

    # Optional: Open in VS Code
    open_in_vscode()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)
