from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from {{ cookiecutter.__package_slug }}.infrastructure.persistence.database import Base
from {{ cookiecutter.__package_slug }}.domain.entities.task_list import TaskList


class TaskListModel(Base):
    """SQLAlchemy ORM model for TaskList aggregate."""

    __tablename__ = "task_lists"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @staticmethod
    def from_domain(entity: TaskList) -> "TaskListModel":
        return TaskListModel(
            id=entity.id,
            name=entity.name,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def to_domain(self) -> TaskList:
        return TaskList(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
