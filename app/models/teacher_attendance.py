from sqlalchemy import Column, Integer, Date, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class TeacherStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    leave = "leave"


class TeacherAttendance(Base):
    __tablename__ = "teacher_attendance"

    id = Column(Integer, primary_key=True)

    teacher_id = Column(Integer, ForeignKey("teachers.id"))
    date = Column(Date)
    status = Column(Enum(TeacherStatus))

    teacher = relationship("Teacher")

    __table_args__ = (
        UniqueConstraint("teacher_id", "date", name="uq_teacher_date"),
    )