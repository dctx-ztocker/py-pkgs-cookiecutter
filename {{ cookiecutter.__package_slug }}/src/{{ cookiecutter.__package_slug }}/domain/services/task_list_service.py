from datetime import datetime, timezone
from typing import List

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList
from {{ cookiecutter.__package_slug }}.domain.repositories.task_list_repository import TaskListRepository


class TaskListService:
    """Domain service for operations on TaskList aggregates.

    This encapsulates business rules around creating and listing task lists,
    relying only on the repository interface.
    """

    def __init__(self, repo: TaskListRepository) -> None:
        self._repo = repo

    def create(self, name: str) -> TaskList:
        """Create a new task list with the provided name.

        Ensures timestamps are set using UTC.
        """
        entity = TaskList(name=name, created_at=datetime.now(timezone.utc))
        return self._repo.create(entity)

    def list(self, *, offset: int = 0, limit: int = 100) -> List[TaskList]:
        """Return a paginated collection of task lists."""
        return self._repo.list(offset=offset, limit=limit)
