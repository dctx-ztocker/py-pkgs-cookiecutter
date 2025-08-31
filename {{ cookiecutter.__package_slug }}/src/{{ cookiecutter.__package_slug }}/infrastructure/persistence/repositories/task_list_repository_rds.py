from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList
from {{ cookiecutter.__package_slug }}.domain.repositories.task_list_repository import TaskListRepository
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.models.task_list import TaskListModel


class TaskListRepositoryRds(TaskListRepository):
    """Relational DB repository for TaskList using SQLAlchemy Session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, task_list_id: UUID) -> Optional[TaskList]:
        model = self._session.get(TaskListModel, task_list_id)
        return model.to_domain() if model else None

    def list(self, *, offset: int = 0, limit: int = 100) -> List[TaskList]:
        stmt = select(TaskListModel).offset(offset).limit(limit)
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def create(self, task_list: TaskList) -> TaskList:
        """Persist a new TaskList and return the stored entity."""
        model = TaskListModel.from_domain(task_list)
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return model.to_domain()

    def update(self, task_list: TaskList) -> TaskList:
        """Update an existing TaskList; raises KeyError if not found."""
        existing = self._session.get(TaskListModel, task_list.id)
        if existing is None:
            raise KeyError("TaskList not found")
        existing.name = task_list.name
        existing.created_at = task_list.created_at
        existing.updated_at = task_list.updated_at
        self._session.flush()
        self._session.refresh(existing)
        return existing.to_domain()

    def delete(self, task_list_id: UUID) -> bool:
        """Delete a TaskList by id and return True if it existed."""
        model = self._session.get(TaskListModel, task_list_id)
        if model is None:
            return False
        self._session.delete(model)
        # Ensure deletion is visible within the same session
        self._session.flush()
        # Remove from identity map so subsequent get() won't return cached instance
        self._session.expunge(model)
        return True
