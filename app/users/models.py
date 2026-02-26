from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    func,
    ForeignKey,
    text,
)
from core.database import Base
from sqlalchemy.orm import relationship
from passlib.context import CryptContext

from enum import Enum
from sqlalchemy import Enum as SQLEnum


pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
)


class UserType(str, Enum):
    ADMIN = "admin"
    USER = "user"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(250), unique=True, nullable=False)
    # define as a SQLAlchemy Column (not a type annotation) so the ORM and
    # Alembic can detect and generate migrations for the enum correctly
    # give a server_default so adding the column in SQLite works during migrations
    user_type = Column(
        SQLEnum(UserType, name="user_type_enum"),
        nullable=False,
        default=UserType.USER,
        server_default=text("'USER'"),
    )

    password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)

    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(
        DateTime, server_default=func.now(), server_onupdate=func.now()
    )

    tasks = relationship("TaskModel", back_populates="user")

    def hash_password(self, plain_password: str) -> None:
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.password)

    def set_password(self, plain_text: str) -> None:
        self.password = self.hash_password(plain_text)


class TokenModel(Base):
    __tablename__ = "tokens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    token = Column(String, unique=True, nullable=False)
    created_date = Column(DateTime, default=func.now(), nullable=False)
    # add expire date

    user = relationship("UserModel", uselist=False)
