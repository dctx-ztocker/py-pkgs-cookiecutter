from fastapi import FastAPI
from importlib.metadata import version, metadata

from {{ cookiecutter.__package_slug }}.infrastructure.container import Container
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.task_lists import router as task_lists_router
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.tasks import router as tasks_router
from {{ cookiecutter.__package_slug }}.infrastructure.web.ui.routes import router as ui_router


def create_app() -> FastAPI:
    """FastAPI application factory with container-based initialization."""
    container = Container()
    container.init_database()

    # Get package metadata
    package_version = version("{{ cookiecutter.__package_slug }}")
    package_metadata = metadata("{{ cookiecutter.__package_slug }}")
    package_name = package_metadata.get("Name", "{{ cookiecutter.__package_slug }}")
    package_description = package_metadata.get(
        "Summary", "A package for doing great things!"
    )

    app = FastAPI(
        title=package_name.title(),
        version=package_version,
        description=package_description,
    )
    app.container = container  # type: ignore[attr-defined]

    app.include_router(task_lists_router)
    app.include_router(tasks_router)
    app.include_router(ui_router)

    return app


app = create_app()
