from fastapi import APIRouter, Path
from typing import Annotated

router = APIRouter(tags=["tasks"])


@router.get("/tasks")
async def retrevie_task_list():
    return []


@router.get("/tasks/{task_id}")
async def retrevie_single_task_detail(task_id: Annotated[int, Path(..., gt=0)]):
    return {}


@router.post("/tasks")
async def create_task():
    return {}


@router.put("/tasks/{task_id}")
async def update_task(task_id: Annotated[int, Path(..., gt=0)]):
    return {}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: Annotated[int, Path(..., gt=0)]):
    return {}
