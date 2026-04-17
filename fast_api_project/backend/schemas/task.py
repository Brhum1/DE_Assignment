from pydantic import BaseModel

class TaskBase(BaseModel):
    title: str
    is_completed: bool = False

class TaskCreate(TaskBase):
    project_id: int

class TaskUpdate(BaseModel):
    title: str | None = None
    is_completed: bool | None = None

class TaskOut(TaskBase):
    id: int
    project_id: int

    class Config:
        from_attributes = True