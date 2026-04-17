from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(10), nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"))
    class_obj = relationship("Class", back_populates="sections")