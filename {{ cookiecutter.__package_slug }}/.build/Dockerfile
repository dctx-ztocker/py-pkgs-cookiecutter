# Use official Python image matching the version in pyproject.toml
FROM python:{{ cookiecutter.python_version }}-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_CACHE_DIR="/tmp/poetry_cache" \
    POETRY_VENV_IN_PROJECT=1 \
    POETRY_NO_INTERACTION=1

# Install Poetry
RUN pip install poetry

# Create application directory
WORKDIR /app

# Copy poetry configuration files
COPY pyproject.toml poetry.lock* ./

# Configure poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-root \
    && rm -rf $POETRY_CACHE_DIR

# Copy application code
COPY . .

# Build the package using poetry
RUN poetry build

# Install the built package using pip
RUN pip install dist/*.whl

# Create a non-root user
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Default command
CMD ["python", "-m", "{{ cookiecutter.__package_slug }}"]
