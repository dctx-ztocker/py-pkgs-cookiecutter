from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TaskList(BaseModel):
    """Domain entity representing a list of tasks."""

    id: UUID = Field(default_factory=uuid4)
    name: str = Field(min_length=1, max_length=120)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def rename(self, new_name: str) -> None:
        """Rename the task list ensuring non-empty name and update timestamp."""
        if not new_name or not new_name.strip():
            raise ValueError("name cannot be empty")
        self.name = new_name
        self.updated_at = datetime.now(timezone.utc)
