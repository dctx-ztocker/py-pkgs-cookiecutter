from pydantic import BaseModel

from {{ cookiecutter.__package_slug }}.domain.entities.task import Task


class TaskOut(BaseModel):
    """Output model for Task endpoints."""

    id: str
    task_list_id: str
    title: str
    is_completed: bool

    @staticmethod
    def from_domain(entity: Task) -> "TaskOut":
        return TaskOut(
            id=str(entity.id),
            task_list_id=str(entity.task_list_id),
            title=entity.title,
            is_completed=entity.is_completed,
        )
