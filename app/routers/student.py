from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.student import Student
from app.schemas.student import StudentCreate
from app.core.permissions import require_permission

router = APIRouter(prefix="/students", tags=["Students"])


@router.post("/", dependencies=[Depends(require_permission("create_student"))])
def create_student(data: StudentCreate, db: Session = Depends(get_db)):

    new_student = Student(
        user_id=data.user_id,
        class_id=data.class_id,
        section_id=data.section_id,
        roll_number=data.roll_number
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student