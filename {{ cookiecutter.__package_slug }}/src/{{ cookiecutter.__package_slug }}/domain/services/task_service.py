from datetime import datetime, timezone
from typing import List
from uuid import UUID

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task
from {{ cookiecutter.__package_slug }}.domain.repositories.task_repository import TaskRepository


class TaskService:
    """Domain service for operations on Task entities.

    Provides orchestration for adding, completing and listing tasks while
    deferring persistence to the repository interface.
    """

    def __init__(self, repo: TaskRepository) -> None:
        self._repo = repo

    def add(
        self, task_list_id: UUID, title: str, description: str | None = None
    ) -> Task:
        """Create and persist a new task within a given task list."""
        entity = Task(
            task_list_id=task_list_id,
            title=title,
            description=description,
            created_at=datetime.now(timezone.utc),
        )
        return self._repo.create(entity)

    def complete(self, task_id: UUID) -> Task:
        """Mark a task as completed and persist the change.

        Raises KeyError if the task does not exist.
        """
        existing = self._repo.get(task_id)
        if existing is None:
            raise KeyError("Task not found")
        existing.mark_completed()
        return self._repo.update(existing)

    def list(
        self, task_list_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> List[Task]:
        """Return a paginated collection of tasks for a given list."""
        return self._repo.list_by_task_list(task_list_id, offset=offset, limit=limit)
