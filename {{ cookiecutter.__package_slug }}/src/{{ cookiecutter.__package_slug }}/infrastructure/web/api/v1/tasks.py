from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends

from {{ cookiecutter.__package_slug }}.application.tasks import TaskUseCases
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.schemas.task_create_in import TaskCreateIn
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.schemas.task_out import TaskOut
from {{ cookiecutter.__package_slug }}.infrastructure.web.dependencies.services import get_task_use_cases


router = APIRouter(prefix="/tasks", tags=["tasks"])


# Removed local DTOs; importing from schemas instead


@router.post("/", response_model=TaskOut, summary="Create a task")
def create(
    payload: TaskCreateIn,
    use_cases: TaskUseCases = Depends(get_task_use_cases),
) -> TaskOut:
    created = use_cases.add(payload.task_list_id, payload.title, payload.description)
    return TaskOut.from_domain(created)


@router.post("/{task_id}/complete", response_model=TaskOut, summary="Complete a task")
def complete(
    task_id: UUID,
    use_cases: TaskUseCases = Depends(get_task_use_cases),
) -> TaskOut:
    updated = use_cases.complete(task_id)
    return TaskOut.from_domain(updated)


@router.get(
    "/by-list/{task_list_id}",
    response_model=List[TaskOut],
    summary="List tasks by list id",
)
def list_by_list(
    task_list_id: UUID,
    offset: int = 0,
    limit: int = 100,
    use_cases: TaskUseCases = Depends(get_task_use_cases),
) -> List[TaskOut]:
    items = use_cases.list(task_list_id, offset=offset, limit=limit)
    return [TaskOut.from_domain(x) for x in items]
