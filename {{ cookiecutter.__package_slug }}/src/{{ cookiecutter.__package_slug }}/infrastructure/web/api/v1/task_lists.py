from typing import List

from fastapi import APIRouter, Depends

from {{ cookiecutter.__package_slug }}.application.task_lists import TaskListUseCases
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.schemas.task_list_create_in import TaskListCreateIn
from {{ cookiecutter.__package_slug }}.infrastructure.web.api.v1.schemas.task_list_out import TaskListOut
from {{ cookiecutter.__package_slug }}.infrastructure.web.dependencies.services import get_task_list_use_cases


router = APIRouter(prefix="/task-lists", tags=["task-lists"])


@router.post("/", response_model=TaskListOut, summary="Create a task list")
def create(
    payload: TaskListCreateIn,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases),
) -> TaskListOut:
    created = use_cases.create(payload.name)
    return TaskListOut.from_domain(created)


@router.get("/", response_model=List[TaskListOut], summary="List task lists")
def list_(
    offset: int = 0,
    limit: int = 100,
    use_cases: TaskListUseCases = Depends(get_task_list_use_cases),
) -> List[TaskListOut]:
    items = use_cases.list(offset=offset, limit=limit)
    return [TaskListOut.from_domain(x) for x in items]
