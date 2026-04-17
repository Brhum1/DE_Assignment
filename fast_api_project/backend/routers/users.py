from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserOut
from typing import List

router = APIRouter()

# 1. إنشاء مستخدم جديد (Register)
@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="الايميل مسجل مسبقاً")
    
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # ملاحظة: سنضيف التشفير لاحقاً
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# 2. جلب جميع المستخدمين (خاص بالأدمن)
@router.get("/", response_model=List[UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# 3. حذف مستخدم (خاص بالأدمن)
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    # سيتم حذف مشاريع المستخدم ومهامه تلقائياً إذا فعلت الـ Cascade في الموديل
    db.delete(db_user)
    db.commit()
    return {"message": "تم حذف المستخدم بنجاح"}

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_data: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="المستخدم غير موجود")
    
    db_user.username = user_data.username
    db_user.email = user_data.email
    if user_data.password:
        db_user.hashed_password = user_data.password # سنضيف التشفير لاحقاً
        
    db.commit()
    db.refresh(db_user)
    return db_user