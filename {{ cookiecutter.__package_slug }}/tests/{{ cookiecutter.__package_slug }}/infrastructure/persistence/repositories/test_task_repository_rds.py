from datetime import datetime, timezone

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task
from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.database import Base
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.repositories.task_list_repository_rds import (
    TaskListRepositoryRds,
)
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.repositories.task_repository_rds import (
    TaskRepositoryRds,
)


def setup_in_memory_db():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal


def test_task_crud_pagination_and_post_delete_get():
    engine, SessionLocal = setup_in_memory_db()
    with SessionLocal() as session:  # type: Session
        task_list_repo = TaskListRepositoryRds(session)
        repo = TaskRepositoryRds(session)

        tl = task_list_repo.create(
            TaskList(name="Inbox", created_at=datetime.now(timezone.utc))
        )
        t1 = repo.create(
            Task(task_list_id=tl.id, title="t1", created_at=datetime.now(timezone.utc))
        )
        t2 = repo.create(
            Task(task_list_id=tl.id, title="t2", created_at=datetime.now(timezone.utc))
        )
        _t3 = repo.create(
            Task(task_list_id=tl.id, title="t3", created_at=datetime.now(timezone.utc))
        )

        page1 = repo.list_by_task_list(tl.id, offset=0, limit=2)
        page2 = repo.list_by_task_list(tl.id, offset=2, limit=2)
        assert len(page1) == 2
        assert len(page2) == 1

        got = repo.get(t1.id)
        assert got is not None and got.title == "t1"

        t1.mark_completed()
        t1u = repo.update(t1)
        assert t1u.is_completed and t1u.completed_at is not None

        ok = repo.delete(t2.id)
        assert ok is True
        assert repo.get(t2.id) is None
