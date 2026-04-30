from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models import parent_student
from app.models.parent import Parent
from app.schemas.parent import ParentCreate
from app.core.permissions import require_permission


router = APIRouter(prefix="/parents", tags=["Parents"])


@router.post("/", dependencies=[Depends(require_permission("create_parent"))])
def create_parent(data: ParentCreate, db: Session = Depends(get_db)):

    parent = Parent(user_id=data.user_id)

    db.add(parent)
    db.commit()
    db.refresh(parent)

    return parent

@router.post("/link")
def link_parent_student(parent_id: int, student_id: int, db: Session = Depends(get_db)):

    db.execute(
        parent_student.insert().values(
            parent_id=parent_id,
            student_id=student_id
        )
    )

    db.commit()

    return {"message": "Linked successfully"}