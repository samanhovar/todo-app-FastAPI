from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from core.database import Base
from sqlalchemy.orm import relationship


class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    user = relationship("UserModel", back_populates="tasks", uselist=False)
