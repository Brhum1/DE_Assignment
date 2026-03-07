from pydantic import BaseModel
from typing import Optional, List

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    owner_id: int

class ProjectOut(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True