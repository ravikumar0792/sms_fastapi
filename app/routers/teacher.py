from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.teacher import Teacher
from app.schemas.teacher import TeacherCreate
from app.core.permissions import require_permission


router = APIRouter(prefix="/teachers", tags=["Teachers"])


@router.post("/", dependencies=[Depends(require_permission("create_teacher"))])
def create_teacher(data: TeacherCreate, db: Session = Depends(get_db)):

    teacher = Teacher(user_id=data.user_id)

    db.add(teacher)
    db.commit()
    db.refresh(teacher)

    return teacher