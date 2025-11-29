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

    # Relación con Subject (one-to-many)
    subjects: so.Mapped[list["Subject"]] = so.relationship(
        "Subject",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    
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
    name: so.Mapped[str] = so.mapped_column(sa.String(100), index=True)
    description: so.Mapped[str] = so.mapped_column(sa.String(512))

    total_hours_goal: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)
    total_hours_completed: so.Mapped[int] = so.mapped_column(sa.Integer, default=0)

    created_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now(timezone.utc), index=True)
    updated_at: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    priority_level: so.Mapped[PriorityLevel] = so.mapped_column(SqlEnum(PriorityLevel), default=PriorityLevel.MEDIUM, index=True)
    status: so.Mapped[SubjectStatus] = so.mapped_column(SqlEnum(SubjectStatus), default=SubjectStatus.ACTIVE)

    # Relación con User (many-to-one)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=False)
    user: so.Mapped[User] = so.relationship("User", back_populates="subjects")

    __table_args__ = (
        sa.Index("idx_subject_user_status", "user_id", "status"), #compuesto
    )
    # Relación con Sessions (one-to-many)
    study_sessions: so.Mapped[list["StudySessions"]] = so.relationship(
        "StudySessions",
        back_populates="subject",
        cascade="all, delete-orphan"
    )


class StudySessions(db.Model):
    __tablename__ = "study_sessions"

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    start_time: so.Mapped[datetime] = so.mapped_column(sa.DateTime, default=datetime.now(timezone.utc))
    end_time: so.Mapped[Optional[datetime]] = so.mapped_column(sa.DateTime, nullable=True, index=True)
    duration_minutes: so.Mapped[Optional[int]] = so.mapped_column(sa.Integer, nullable=True)
    notes: so.Mapped[str] = so.mapped_column(sa.String(2048), default="")

    
    subject_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("subject.id"), nullable=False, index=True)
    subject: so.Mapped[Subject] = so.relationship("Subject", back_populates="study_sessions")

