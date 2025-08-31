from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task
from {{ cookiecutter.__package_slug }}.domain.repositories.task_repository import TaskRepository
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.models.task import TaskModel


class TaskRepositoryRds(TaskRepository):
    """Relational DB repository for Task using SQLAlchemy Session."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get(self, task_id: UUID) -> Optional[Task]:
        model = self._session.get(TaskModel, task_id)
        return model.to_domain() if model else None

    def list_by_task_list(
        self, task_list_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> List[Task]:
        stmt = (
            select(TaskModel)
            .where(TaskModel.task_list_id == task_list_id)
            .offset(offset)
            .limit(limit)
        )
        rows = self._session.execute(stmt).scalars().all()
        return [m.to_domain() for m in rows]

    def create(self, task: Task) -> Task:
        """Persist a new Task and return the stored entity."""
        model = TaskModel.from_domain(task)
        self._session.add(model)
        self._session.flush()
        self._session.refresh(model)
        return model.to_domain()

    def update(self, task: Task) -> Task:
        """Update an existing Task; raises KeyError if not found."""
        existing = self._session.get(TaskModel, task.id)
        if existing is None:
            raise KeyError("Task not found")
        existing.task_list_id = task.task_list_id
        existing.title = task.title
        existing.description = task.description
        existing.is_completed = task.is_completed
        existing.created_at = task.created_at
        existing.completed_at = task.completed_at
        self._session.flush()
        self._session.refresh(existing)
        return existing.to_domain()

    def delete(self, task_id: UUID) -> bool:
        """Delete a Task by id and return True if it existed."""
        model = self._session.get(TaskModel, task_id)
        if model is None:
            return False
        self._session.delete(model)
        # Ensure deletion is visible within the same session
        self._session.flush()
        # Remove from identity map so subsequent get() won't return cached instance
        self._session.expunge(model)
        return True
