from flask import request, jsonify
from app.models import StudySessions, Subject
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.study_sessions_schema import StudySessionsSchema, EditStudySessionsSchema # Fixed import

from datetime import datetime, timezone

study_sessions_bp = Blueprint("sessions", "sessions", url_prefix="/sessions")

#LOS 4 CRUD ENDPOINTS

@study_sessions_bp.route("")
class StudySessionListCreate(MethodView):
    @jwt_required()
    @study_sessions_bp.arguments(StudySessionsSchema)
    @study_sessions_bp.response(201)
    def post(self, session_data):
        """Create a new session for the subject for the current user"""
        current_user_id = int(get_jwt_identity())

        # Extract subject_id from the payload
        subject_id = session_data["subject_id"]

        # Verify subject belongs to the user
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user_id).first()
        if not subject:
            return {"error": "Subject not found or unauthorized"}, 403

        new_session = StudySessions(
            start_time=session_data["start_time"],
            end_time=session_data["end_time"],
            duration_minutes=session_data["duration_minutes"],
            subject_id=subject_id
        )

        db.session.add(new_session)
        db.session.commit()
        return {
            "message": "Session added successfully",
            "id": new_session.id,
            "subject_id": new_session.subject_id
        }, 201
    
    @jwt_required()
    def get(self):
        """Get all sessions for the current subject"""
        current_user_id = int(get_jwt_identity())

        user_subjects = Subject.query.filter_by(user_id=current_user_id).all()
        subject_ids = [s.id for s in user_subjects]
        sessions = StudySessions.query.filter(
            StudySessions.subject_id.in_(subject_ids)
        ).all()

        result = [
            {
                "session_id": ses.id,
                "subject_id": ses.subject_id,
                "start_time": ses.start_time,
                "end_time": ses.end_time,
                "duration_minutes": ses.duration_minutes
            }
            for ses in sessions
        ]

        return result, 200
    
@study_sessions_bp.route("/<int:id>")
class StudySessionDetail(MethodView):
    @jwt_required()
    @study_sessions_bp.arguments(EditStudySessionsSchema)
    @study_sessions_bp.response(200)
    def put(self, session_data):
        pass