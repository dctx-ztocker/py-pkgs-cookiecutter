from pydantic import BaseModel, Field


class TaskListCreateIn(BaseModel):
    """Input payload to create a TaskList."""

    name: str = Field(min_length=1, max_length=120)
