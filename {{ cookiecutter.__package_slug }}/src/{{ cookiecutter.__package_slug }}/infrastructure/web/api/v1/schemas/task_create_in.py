from uuid import UUID

from pydantic import BaseModel, Field


class TaskCreateIn(BaseModel):
    """Input payload to create a Task within a list."""

    task_list_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
