from typing import List, Optional, Protocol, runtime_checkable
from uuid import UUID

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task


@runtime_checkable
class TaskRepository(Protocol):
    """Abstraction for persisting and retrieving Task entities."""

    def get(self, task_id: UUID) -> Optional[Task]: ...

    def list_by_task_list(
        self, task_list_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> List[Task]: ...

    def create(self, task: Task) -> Task: ...

    def update(self, task: Task) -> Task: ...

    def delete(self, task_id: UUID) -> bool: ...
