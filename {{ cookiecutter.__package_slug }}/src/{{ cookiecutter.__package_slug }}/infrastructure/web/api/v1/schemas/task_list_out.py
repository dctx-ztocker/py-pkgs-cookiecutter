from pydantic import BaseModel

from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList


class TaskListOut(BaseModel):
    """Output model for TaskList endpoints."""

    id: str
    name: str

    @staticmethod
    def from_domain(entity: TaskList) -> "TaskListOut":
        return TaskListOut(id=str(entity.id), name=entity.name)
