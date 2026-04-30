from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base_class import Base

teacher_subject = Table(
    "teacher_subject",
    Base.metadata,
    Column("teacher_id", Integer, ForeignKey("teachers.id")),
    Column("subject_id", Integer, ForeignKey("subjects.id")),
)