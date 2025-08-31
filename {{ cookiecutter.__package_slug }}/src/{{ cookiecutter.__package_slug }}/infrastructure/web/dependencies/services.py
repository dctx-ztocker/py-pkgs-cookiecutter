from fastapi import Depends
from sqlalchemy.orm import Session

from {{ cookiecutter.__package_slug }}.application.task_lists import TaskListUseCases
from {{ cookiecutter.__package_slug }}.application.tasks import TaskUseCases
from {{ cookiecutter.__package_slug }}.domain.services.task_list_service import (
    TaskListService as DomainTaskListService,
)
from {{ cookiecutter.__package_slug }}.domain.services.task_service import TaskService as DomainTaskService
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.repositories.task_list_repository_rds import (
    TaskListRepositoryRds,
)
from {{ cookiecutter.__package_slug }}.infrastructure.persistence.repositories.task_repository_rds import (
    TaskRepositoryRds,
)
from {{ cookiecutter.__package_slug }}.infrastructure.web.dependencies.db import get_session


def get_task_list_use_cases(
    session: Session = Depends(get_session),
) -> TaskListUseCases:
    """Build TaskList use cases with RDS repository and domain service."""
    repo = TaskListRepositoryRds(session)
    svc = DomainTaskListService(repo)
    return TaskListUseCases(svc)


def get_task_use_cases(session: Session = Depends(get_session)) -> TaskUseCases:
    """Build Task use cases with RDS repository and domain service."""
    repo = TaskRepositoryRds(session)
    svc = DomainTaskService(repo)
    return TaskUseCases(svc)
