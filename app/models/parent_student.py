from sqlalchemy import Table, Column, Integer, ForeignKey
from app.db.base_class import Base

parent_student = Table(
    "parent_student",
    Base.metadata,
    Column("parent_id", Integer, ForeignKey("parents.id")),
    Column("student_id", Integer, ForeignKey("students.id")),
)