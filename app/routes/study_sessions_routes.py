from flask import request, jsonify
from app.models import StudySessions, Subject
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.study_sessions_schema import StudySessionsSchema, EditStudySessionsSchema # Fixed import
from app.utils.limiters import limiter

from datetime import datetime, timezone

study_sessions_bp = Blueprint("sessions", "sessions", url_prefix="/sessions")

#LOS 4 CRUD ENDPOINTS

@study_sessions_bp.route("")
class StudySessionListCreate(MethodView):
    @jwt_required()
    @study_sessions_bp.arguments(StudySessionsSchema)
    @study_sessions_bp.response(201)
    @limiter.limit("70 per hour")
    def post(self, session_data):
        """Create a new session for the subject for the current user"""
        current_user_id = int(get_jwt_identity())

        # Extract subject_id from the payload
        subject_id = session_data["subject_id"]

        # Verify subject belongs to the user
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user_id).first()
        if not subject:
            return {"error": "Subject not found or unauthorized"}, 403

        start = datetime.strptime(session_data["start_time"], "%I:%M%p")
        end = datetime.strptime(session_data["end_time"], "%I:%M%p")

        duration = int((end - start).total_seconds() // 60)

        new_session = StudySessions(
            start_time=start,
            end_time=end,
            duration_minutes=duration,
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
    @limiter.limit("90 per hour")
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
                "start_time": ses.start_time.isoformat() if ses.start_time else None,
                "end_time": ses.end_time.isoformat() if ses.end_time else None,
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
    @limiter.limit("70 per hour")
    def put(self, session_data, id):
        """Update a study session"""
        current_user_id = int(get_jwt_identity())

        session = StudySessions.query.get(id)
        if not session:
            return {"error": "Session not found"}, 404

        subject = Subject.query.filter_by(
            id=session.subject_id,
            user_id=current_user_id
        ).first()

        if not subject:
            return {"error": "Unauthorized"}, 403
        
        start = datetime.strptime(session_data["start_time"], "%I:%M%p")
        end = datetime.strptime(session_data["end_time"], "%I:%M%p")
        duration = int((end - start).total_seconds() // 60)

        session.start_time = start
        session.end_time = end
        session.duration_minutes = duration
        db.session.commit()
        return {"message": "Session updated successfully"}, 200
    
    @jwt_required()
    @limiter.limit("50 per hour")
    def delete(self, id):
        current_user_id = int(get_jwt_identity())

        session = StudySessions.query.get(id)
        if not session:
            return {"error": "Session not found"}, 404
        
        subject = Subject.query.filter_by(
            id=session.subject_id,
            user_id=current_user_id
        ).first()

        if not subject:
            return {"error": "Unauthorized"}, 403
        
        db.session.delete(session)
        db.session.commit()

        return {"message": "Session deleted"}, 200
