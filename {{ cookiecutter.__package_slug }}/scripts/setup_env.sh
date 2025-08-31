#!/usr/bin/env bash

set -euo pipefail

# Output mode flags
QUIET=1
case "${1:-}" in
  --verbose) QUIET=0 ;;
  --quiet) QUIET=1 ;;
  *) : ;;
esac

# Track whether we performed any action (e.g., created env, installed tools)
DID_ACTION=0

# Preserve a handle to the original stdout and optionally silence regular output
if [[ "$QUIET" -eq 1 ]]; then
  exec 3>&1
  exec 1>/dev/null
else
  exec 3>&1
fi

supports_color() { [[ -t 3 ]] && command -v tput >/dev/null 2>&1; }
color_green() { supports_color && tput setaf 2 || true; }
color_yellow() { supports_color && tput setaf 3 || true; }
color_red() { supports_color && tput setaf 1 || true; }
color_reset() { supports_color && tput sgr0 || true; }

print_status_line() {
  local level="$1"; shift || true
  local msg="$*"
  case "$level" in
    OK)
      { color_green; printf "%s\n" "$msg"; color_reset; } >&3
      ;;
    WARN)
      { color_yellow; printf "%s\n" "$msg"; color_reset; } >&3
      ;;
    ERR)
      { color_red; printf "%s\n" "$msg"; color_reset; } >&3
      ;;
    *)
      printf "%s\n" "$msg" >&3
      ;;
  esac
}

# Print compact status: static prefix uncolored, status+emoji colored
print_status_compact() {
  local level="$1"; shift || true
  local status_text="$1"; shift || true
  local emoji="$1"; shift || true
  local STATUS_UPPER
  STATUS_UPPER=$(printf "%s" "$status_text" | tr '[:lower:]' '[:upper:]')
  case "$level" in
    OK)
      {
        printf "Environment status: "
        color_green; printf "%s %s\n" "$STATUS_UPPER" "$emoji"; color_reset
      } >&3
      ;;
    WARN)
      {
        printf "Environment status: "
        color_yellow; printf "%s %s\n" "$STATUS_UPPER" "$emoji"; color_reset
      } >&3
      ;;
    ERR)
      {
        printf "Environment status: "
        color_red; printf "%s %s\n" "$STATUS_UPPER" "$emoji"; color_reset
      } >&3
      ;;
    *)
      printf "Environment status: %s %s\n" "$STATUS_UPPER" "$emoji" >&3
      ;;
  esac
}

has_pyenv() {
  command -v pyenv >/dev/null 2>&1
}

has_pyenv_virtualenv() {
  has_pyenv && pyenv commands 2>/dev/null | grep -Eq '^[[:space:]]*virtualenv([[:space:]]|$)'
}

read_pyproject_python_constraint() {
  if [[ ! -f pyproject.toml ]]; then
    return 1
  fi
  sed -n '/^\[tool\.poetry\.dependencies\]/,/^\[/p' pyproject.toml \
    | grep -E '^[[:space:]]*python[[:space:]]*=' | head -n1 \
    | sed -E 's/^[^=]*=[[:space:]]*"?([^"#]+)"?.*/\1/' \
    | tr -d '[:space:]'
}

resolve_exact_python_version() {
  echo "$1" | sed -n 's/^[^0-9]*//p' | grep -Eo '[0-9]+(\.[0-9]+){2}' | head -n1
}

read_project_name() {
  if [[ ! -f pyproject.toml ]]; then
    return 1
  fi
  sed -n '/^\[tool\.poetry\]/,/^\[/p' pyproject.toml \
    | grep -E '^[[:space:]]*name[[:space:]]*=' | head -n1 \
    | sed -E 's/^[^=]*=[[:space:]]*"?([^"#]+)"?.*/\1/' \
    | tr -d '[:space:]'
}

read_local_env_name() {
  if [[ -f .python-version ]]; then
    head -n1 .python-version | tr -d '[:space:]'
  fi
}

check_project_virtualenv() {
  local version="$1"
  local env_name local_name project_name
  local_name=$(read_local_env_name || true)
  project_name=$(read_project_name || true)

  if [[ -n "${local_name:-}" ]]; then
    env_name="$local_name"
  elif [[ -n "${project_name:-}" ]]; then
    env_name="$project_name"
    echo "project name: $env_name"
  else
    echo "env name: MISSING"
    return 1
  fi

  # Prefer explicit match: version/envs/name should appear in pyenv list
  local env_entry="${version}/envs/${env_name}"
  if pyenv versions --bare | grep -Fxq "$env_entry"; then
    echo "pyenv entry ${env_entry}: OK"
    return 0
  fi
  # Fallback: some pyenv setups require prefix check for env entries
  if pyenv prefix "$env_entry" >/dev/null 2>&1; then
    echo "pyenv entry ${env_entry}: OK"
    return 0
  fi
  echo "pyenv entry ${env_entry}: MISSING"
  return 1
}

create_project_virtualenv() {
  local version="$1"
  local env_name local_name project_name
  local_name=$(read_local_env_name || true)
  project_name=$(read_project_name || true)

  if [[ -n "${local_name:-}" ]]; then
    env_name="$local_name"
  elif [[ -n "${project_name:-}" ]]; then
    env_name="$project_name"
  else
    echo "env name: MISSING"
    return 1
  fi

  local env_entry="${version}/envs/${env_name}"
  print_status_compact WARN "missing -> installing ${env_entry}" "🟡"
  pyenv virtualenv "$version" "$env_name"
  pyenv local "$env_name"
  local prefix
  prefix=$(pyenv prefix "$env_name")
  "$prefix/bin/python" -m pip install --upgrade pip
  "$prefix/bin/python" -m pip install "poetry==2.1.3"

  # Install project dependencies
  print_status_compact WARN "installing dependencies" "📦"
  "$prefix/bin/poetry" install
  DID_ACTION=1

  # Verify
  if pyenv versions --bare | grep -Fxq "$env_entry" || pyenv prefix "$env_entry" >/dev/null 2>&1; then
    echo "pyenv entry ${env_entry}: OK"
    return 0
  fi
  echo "pyenv entry ${env_entry}: MISSING"
  return 1
}

check_python_version_in_pyenv() {
  local constraint
  constraint=$(read_pyproject_python_constraint || true)
  if [[ -z "${constraint:-}" ]]; then
    echo "pyproject/python: MISSING"
    return 1
  fi
  echo "python constraint: $constraint"
  local version
  version=$(resolve_exact_python_version "$constraint" || true)
  if [[ -z "${version:-}" ]]; then
    echo "python version: UNRESOLVED (need x.y.z in constraint)"
    return 1
  fi
  # Check presence via pyenv list (base), any env under that version, or prefix fallback
  if pyenv versions --bare | grep -Fxq "$version"; then
    echo "pyenv entry $version: OK"
    return 0
  fi
  if pyenv versions --bare | grep -Eq "^${version}/envs/"; then
    echo "pyenv entry ${version} (via envs): OK"
    return 0
  fi
  if pyenv prefix "$version" >/dev/null 2>&1; then
    echo "pyenv entry $version: OK"
    return 0
  fi
  echo "pyenv entry $version: MISSING"
  return 1
}

main() {
  local missing=0

  if ! has_pyenv; then
    missing=1
  fi
  if ! has_pyenv_virtualenv; then
    missing=1
  fi

  # Conditional next step: only verify Python version in pyenv if basics are present
  if [[ "$missing" -eq 0 ]]; then
    if check_python_version_in_pyenv; then
      # If Python base version exists, verify project virtualenv association
      local constraint version
      constraint=$(read_pyproject_python_constraint || true)
      version=$(resolve_exact_python_version "$constraint" || true)
      if ! check_project_virtualenv "$version"; then
        # Attempt to create the missing env
        if ! create_project_virtualenv "$version"; then
          missing=1
        fi
      fi
    else
      missing=1
    fi
  fi

  # Emit a single concise status line to original stdout (fd 3)
  if [[ "$missing" -eq 0 ]]; then
    if [[ "$DID_ACTION" -eq 1 ]]; then
      print_status_compact OK "ready (actions performed)" "🟢"
    else
      print_status_compact OK "healthy" "🟢"
    fi
  else
    print_status_compact ERR "issues detected" "🔴"
  fi

  exit "$missing"
}

main "$@"
