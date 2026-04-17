from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.class_model import Class
from app.models.section import Section
from app.models.subject import Subject
from app.models.academic_year import AcademicYear

from app.schemas.classes import ClassCreate
from app.schemas.section import SectionCreate
from app.schemas.subject import SubjectCreate
from app.schemas.academic_year import AcademicYearCreate

from app.core.permissions import require_permission

router = APIRouter(prefix="/academic", tags=["Academic"])

@router.post("/classes", dependencies=[Depends(require_permission("create_class"))])
def create_class(data: ClassCreate, db: Session = Depends(get_db)):

    existing = db.query(Class).filter(Class.name == data.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Class already exists")

    new_class = Class(name=data.name)
    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class

@router.post("/sections", dependencies=[Depends(require_permission("create_section"))])
def create_section(data: SectionCreate, db: Session = Depends(get_db)):

    new_section = Section(name=data.name, class_id=data.class_id)
    db.add(new_section)
    db.commit()
    db.refresh(new_section)

    return new_section

@router.post("/subjects", dependencies=[Depends(require_permission("create_subject"))])
def create_subject(data: SubjectCreate, db: Session = Depends(get_db)):

    new_subject = Subject(name=data.name, class_id=data.class_id)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)

    return new_subject

@router.post("/academic-year", dependencies=[Depends(require_permission("create_academic_year"))])
def create_academic_year(data: AcademicYearCreate, db: Session = Depends(get_db)):

    new_year = AcademicYear(
        name=data.name,
        start_date=data.start_date,
        end_date=data.end_date
    )

    db.add(new_year)
    db.commit()
    db.refresh(new_year)

    return new_year