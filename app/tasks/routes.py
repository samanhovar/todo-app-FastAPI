from fastapi import APIRouter, Path, Query, Depends, HTTPException, status
from typing import Annotated
from tasks.schemas import TaskCreateSchema, TaskResponseSchema, TaskUpdateSchema
from tasks.models import TaskModel

# sqlalchemy imports
from sqlalchemy.orm import Session
from core.database import get_db


router = APIRouter(tags=["tasks"], prefix="/tasks")


@router.get(
    "/tasks", response_model=list[TaskResponseSchema], status_code=status.HTTP_200_OK
)
async def retrevie_task_list(
    db: Annotated[Session, Depends(get_db)],
    completed: Annotated[
        bool | None, Query(description="filter tasks based on being completed or not")
    ] = None,
    limit: Annotated[
        int,
        Query(gt=0, le=50, description="limiting the number of items to retrieve"),
    ] = 10,
    offset: Annotated[
        int, Query(ge=0, description="use for paginating based on passed items")
    ] = 0,
):
    query = db.query(TaskModel)
    if completed is not None:
        query = query.filter_by(is_completed=completed)

    return query.limit(limit).offset(offset).all()


@router.get(
    "/tasks/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def retrevie_single_task_detail(
    task_id: Annotated[int, Path(..., gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")

    return task_obj


@router.post(
    "/tasks", response_model=TaskResponseSchema, status_code=status.HTTP_201_CREATED
)
async def create_task(
    request: TaskCreateSchema,
    db: Annotated[Session, Depends(get_db)],
):
    task_obj = TaskModel(**request.model_dump())
    db.add(task_obj)
    db.commit()
    db.refresh(task_obj)

    return task_obj


@router.put(
    "/tasks/{task_id}",
    response_model=TaskResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def update_task(
    request: TaskUpdateSchema,
    task_id: Annotated[int, Path(..., gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_id:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update fields using setattr
    for field, value in request.model_dump(exclude_unset=True).items():
        setattr(task_obj, field, value)

    db.commit()
    db.refresh(task_obj)

    return task_obj


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: Annotated[int, Path(..., gt=0)],
    db: Annotated[Session, Depends(get_db)],
):
    task_obj = db.query(TaskModel).filter_by(id=task_id).first()
    if not task_obj:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task_obj)
    db.commit()
    return {"message": "Task deleted successfully"}
