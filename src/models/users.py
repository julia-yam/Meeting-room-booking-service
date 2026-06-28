import enum
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base import Base

class UserRole(str, enum.Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"

class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole), 
        default=UserRole.EMPLOYEE, 
        nullable=False
    )