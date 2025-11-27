# tests/test_models.py
from app import db
from app.models import User, Subject, StudySessions
from datetime import datetime


def test_create_subject(app):
    with app.app_context():
        user = User(username="tomi", email="a@a.com")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        subject = Subject(
            name="Math",
            description="Calculus",
            total_hours_goal=10,
            total_hours_completed=0,
            priority_level="HIGH",
            status="ACTIVE",
            user_id=user.id
        )

        db.session.add(subject)
        db.session.commit()

        assert subject.id is not None
        assert subject.user_id == user.id
        assert subject.name == "Math"

def test_create_study_session(app):
    with app.app_context():
        user = User(username="tomi", email="a@a.com")
        user.set_password("123")
        db.session.add(user)
        db.session.commit()

        subject = Subject(
            name="Math",
            description="Calculus",
            total_hours_goal=10,
            total_hours_completed=0,
            priority_level="HIGH",
            status="ACTIVE",
            user_id=user.id
        )

        db.session.add(subject)
        db.session.commit()

        study_session = StudySessions(
            subject_id=subject.id,
            start_time=datetime(2024, 1, 1, 15, 0),  # 3 PM
            end_time=datetime(2024, 1, 1, 16, 0),    # 4 PM
            duration_minutes=60
        )

        db.session.add(study_session)
        db.session.commit()