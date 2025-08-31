from typing import List, Optional, Protocol, runtime_checkable
from uuid import UUID

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList


@runtime_checkable
class TaskListRepository(Protocol):
    """Abstraction for persisting and retrieving TaskList aggregates."""

    def get(self, task_list_id: UUID) -> Optional[TaskList]: ...

    def list(self, *, offset: int = 0, limit: int = 100) -> List[TaskList]: ...

    def create(self, task_list: TaskList) -> TaskList: ...

    def update(self, task_list: TaskList) -> TaskList: ...

    def delete(self, task_list_id: UUID) -> bool: ...
