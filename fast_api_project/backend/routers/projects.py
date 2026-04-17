from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.project import Project
from schemas.project import ProjectCreate, ProjectOut
from typing import List

router = APIRouter()

# 1. إنشاء مشروع جديد
@router.post("/", response_model=ProjectOut)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    db_project = Project(**project.model_dump())
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

# 2. جلب جميع المشاريع
@router.get("/", response_model=List[ProjectOut])
def get_projects(db: Session = Depends(get_db)):
    return db.query(Project).all()

# 3. حذف مشروع (هذا الجزء هو الذي كان ينقصك)
@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db)):
    # جلب المشروع من قاعدة البيانات أولاً
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    # التأكد من وجود المشروع
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # حذف المشروع (سيقوم SQLAlchemy بحذف المهام المرتبطة تلقائياً بسبب الـ cascade)
    db.delete(db_project)
    db.commit()
    
    return {"message": "Project deleted successfully"}