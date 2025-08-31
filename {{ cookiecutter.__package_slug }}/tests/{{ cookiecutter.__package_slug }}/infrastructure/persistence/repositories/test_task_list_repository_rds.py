from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.database import Base
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.repositories.task_list_repository_rds import (
    TaskListRepositoryRds,
)


def setup_in_memory_db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def test_task_list_crud_and_pagination():
    engine, SessionLocal = setup_in_memory_db()
    with SessionLocal() as session:  # type: Session
        repo = TaskListRepositoryRds(session)

        a = repo.create(TaskList(name="A", created_at=datetime.now(timezone.utc)))
        b = repo.create(TaskList(name="B", created_at=datetime.now(timezone.utc)))
        _c = repo.create(TaskList(name="C", created_at=datetime.now(timezone.utc)))

        all_lists = repo.list()
        assert {x.name for x in all_lists} == {"A", "B", "C"}

        page1 = repo.list(offset=0, limit=2)
        page2 = repo.list(offset=2, limit=2)
        assert len(page1) == 2
        assert len(page2) == 1

        # get
        got = repo.get(a.id)
        assert got is not None and got.name == "A"

        # update (rename)
        b.rename("B2")
        b2 = repo.update(b)
        assert b2.name == "B2"
        assert b2.updated_at is not None

        # delete existing then try again
        assert repo.delete(a.id) is True
        assert repo.delete(a.id) is False
        assert repo.get(a.id) is None
