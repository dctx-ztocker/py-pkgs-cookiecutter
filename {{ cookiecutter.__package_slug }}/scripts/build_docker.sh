#!/bin/bash

# Build Docker image for {{ cookiecutter.__package_slug }}
# Usage: ./scripts/build_docker.sh [tag]

# Get version from pyproject.toml
VERSION=$(grep "^version = " pyproject.toml | cut -d'"' -f2)
TAG=${1:-$VERSION}
IMAGE="{{ cookiecutter.__package_slug }}:${TAG}"

echo "Building ${IMAGE}..."

# Check requirements
[ -f "pyproject.toml" ] || { echo "Error: Run from project root"; exit 1; }
[ -f ".build/Dockerfile" ] || { echo "Error: Dockerfile not found"; exit 1; }
command -v docker >/dev/null || { echo "Error: Docker not found"; exit 1; }

# Build image
docker build -t "${IMAGE}" -f .build/Dockerfile .

echo "Done: ${IMAGE}"
