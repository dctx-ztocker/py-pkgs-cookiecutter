from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class Task(BaseModel):
    """Domain entity representing a single task within a task list."""

    id: UUID = Field(default_factory=uuid4)
    task_list_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    is_completed: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    @model_validator(mode="after")
    def _sync_completed_at(self) -> "Task":
        """Ensure completed_at is aligned with is_completed state."""
        if self.is_completed and self.completed_at is None:
            self.completed_at = datetime.now(timezone.utc)
        if not self.is_completed:
            self.completed_at = None
        return self

    def mark_completed(self) -> None:
        """Mark the task as completed and set completion timestamp if needed."""
        if not self.is_completed:
            self.is_completed = True
            self.completed_at = datetime.now(timezone.utc)
