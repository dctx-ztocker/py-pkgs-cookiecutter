from typing import List

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList
from {{ cookiecutter.__package_slug }}.domain.services.task_list_service import (
    TaskListService as DomainTaskListService,
)


class TaskListUseCases:
    """Application use cases for TaskList.

    Coordinates request/response boundaries and delegates domain logic to
    the `TaskListService`.
    """

    def __init__(self, service: DomainTaskListService) -> None:
        self._service = service

    def create(self, name: str) -> TaskList:
        return self._service.create(name)

    def list(self, *, offset: int = 0, limit: int = 100) -> List[TaskList]:
        return self._service.list(offset=offset, limit=limit)
