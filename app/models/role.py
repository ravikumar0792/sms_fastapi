from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models.role_permission import role_permissions


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    is_active = Column(Boolean, default=True)

    permissions = relationship(
        "Permission",
        secondary=role_permissions,
        back_populates="roles"
    )