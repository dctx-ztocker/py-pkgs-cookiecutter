from collections.abc import Generator

from fastapi import Request
from sqlalchemy.orm import Session


def get_session(request: Request) -> Generator[Session, None, None]:
    """FastAPI dependency that yields a SQLAlchemy Session from app container."""
    session_factory = request.app.container.session_factory()  # type: ignore[attr-defined]
    session: Session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
