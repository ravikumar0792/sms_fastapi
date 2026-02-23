from sqlalchemy import Column, Integer, String, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base    
import enum
from datetime import datetime

class UserRole(str, enum.Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"
    

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=False)

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")
    is_active = Column(Boolean, default=True)
    refresh_token = Column(String(255), nullable=True)
    verification_token = Column(String(255), nullable=True)
    verification_token_expiry = Column(DateTime, nullable=True)
    is_verified = Column(Boolean, default=False)
    reset_token = Column(String(512), nullable=True)
    reset_token_expire = Column(DateTime, nullable=True)