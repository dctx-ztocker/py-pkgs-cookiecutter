from typing import List
from uuid import UUID

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task
from {{ cookiecutter.__package_slug }}.domain.services.task_service import TaskService as DomainTaskService


class TaskUseCases:
    """Application use cases for Task.

    Coordinates request/response boundaries and delegates domain logic to
    the `TaskService`.
    """

    def __init__(self, service: DomainTaskService) -> None:
        self._service = service

    def add(
        self, task_list_id: UUID, title: str, description: str | None = None
    ) -> Task:
        return self._service.add(task_list_id, title, description)

    def complete(self, task_id: UUID) -> Task:
        return self._service.complete(task_id)

    def list(
        self, task_list_id: UUID, *, offset: int = 0, limit: int = 100
    ) -> List[Task]:
        return self._service.list(task_list_id, offset=offset, limit=limit)
