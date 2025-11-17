from app import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime, timezone
from enum import Enum
from sqlalchemy import Enum as SqlEnum
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = "user"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    # Relación con Subject (one-to-many: un usuario tiene muchos subjects)
    subjects: so.Mapped[list["Subject"]] = so.relationship("Subject", back_populates="user")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class PriorityLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class SubjectStatus(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"


class Subject(db.Model):
    __tablename__ = "subject"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True, unique=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(512), index=True, unique=True)

    total_hours_goal: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    total_hours_completed: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)

    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now(timezone.utc))
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    priority_level: so.Mapped[PriorityLevel] = so.mapped_column(SqlEnum(PriorityLevel), default=PriorityLevel.MEDIUM)
    status: so.Mapped[SubjectStatus] = so.mapped_column(SqlEnum(SubjectStatus), default=SubjectStatus.ACTIVE)

    # Relación con User (many-to-one: muchos subjects pertenecen a un usuario)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    user: so.Mapped[User] = so.relationship("User", back_populates="subjects")
