from sqlalchemy import Column, Integer, String, Date
from app.db.base_class import Base


class AcademicYear(Base):
    __tablename__ = "academic_years"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), unique=True)  # e.g. 2025-26
    start_date = Column(Date)
    end_date = Column(Date)