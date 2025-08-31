from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from {{ cookiecutter.__package_slug }}.infrastructure.settings import Settings
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.database import Base


def _create_engine_for_url(database_url: str):
    """Create a SQLAlchemy engine with dialect-specific options.

    - For sqlite, we must pass check_same_thread=False.
    - For Postgres (and others), use default options.
    """
    if database_url.startswith("sqlite"):
        return create_engine(database_url, connect_args={"check_same_thread": False})
    return create_engine(database_url)


class Container(containers.DeclarativeContainer):
    """Application IoC container for engine, sessions and configuration."""

    wiring_config = containers.WiringConfiguration(modules=[])

    settings = providers.Singleton(Settings)

    engine = providers.Singleton(
        _create_engine_for_url,
        database_url=providers.Callable(lambda s: s.DATABASE_URL, settings),
    )

    session_factory = providers.Singleton(
        sessionmaker,
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    session = providers.Factory(Session, bind=engine)
    init_database = providers.Callable(
        lambda e: Base.metadata.create_all(bind=e), engine
    )
