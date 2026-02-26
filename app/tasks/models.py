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

    # timestamps: created_date is set once, updated_date should refresh on every update
    # use SQLAlchemy defaults and onupdate so the value changes when the object is modified
    created_date = Column(DateTime, default=func.now(), nullable=False)
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    user = relationship("UserModel", back_populates="tasks", uselist=False)
