from sqlalchemy import Column, Integer, Date, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum


class LeaveStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class Leave(Base):
    __tablename__ = "leaves"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String(255))
    status = Column(Enum(LeaveStatus), default="pending")

    user = relationship("User")