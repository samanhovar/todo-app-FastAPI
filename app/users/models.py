from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    is_active = Column(Boolean, default=True)
    
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())
    
    tasks = relationship("TaskModel", back_populates="user")
    