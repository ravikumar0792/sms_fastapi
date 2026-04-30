from sqlalchemy import Column, Integer, Date, Enum, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class AttendanceStatus(str, enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    leave = "leave"


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    status = Column(Enum(AttendanceStatus))

    is_notified = Column(Boolean, default=False)

    student = relationship("Student")

    __table_args__ = (
        UniqueConstraint("student_id", "date", name="uq_student_date"),
    )