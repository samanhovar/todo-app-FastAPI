from pydantic import BaseModel, Field
from typing import Annotated
from datetime import datetime


class TaskBaseSchema(BaseModel):
    title: Annotated[
        str, Field(..., max_length=150, min_length=3, description="Title of the task")
    ]
    description: Annotated[
        str | None, Field(max_length=500, description="Description of the task")
    ] = None
    is_completed: Annotated[bool, Field(description="State of the task")] = False


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(TaskBaseSchema):
    id: Annotated[int, Field(..., description="Unique identifier of the object")]

    created_date: Annotated[
        datetime, Field(..., description="Creation date and time of the object")
    ]
    updated_date: Annotated[
        datetime, Field(..., description="Updating date and time of the object")
    ]
