from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from {{ cookiecutter.__package_slug }}.infrastructure.persistence.database import Base
from {{ cookiecutter.__package_slug }}.domain.entities.task import Task


class TaskModel(Base):
    """SQLAlchemy ORM model for Task entity."""

    __tablename__ = "tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    task_list_id: Mapped[UUID] = mapped_column(
        ForeignKey("task_lists.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    @staticmethod
    def from_domain(entity: Task) -> "TaskModel":
        return TaskModel(
            id=entity.id,
            task_list_id=entity.task_list_id,
            title=entity.title,
            description=entity.description,
            is_completed=entity.is_completed,
            created_at=entity.created_at,
            completed_at=entity.completed_at,
        )

    def to_domain(self) -> Task:
        return Task(
            id=self.id,
            task_list_id=self.task_list_id,
            title=self.title,
            description=self.description,
            is_completed=self.is_completed,
            created_at=self.created_at,
            completed_at=self.completed_at,
        )
