from flask import request
from app.models import StudySessions, Subject
from app import db, cache
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.study_sessions_schema import StudySessionsSchema, EditStudySessionsSchema # Fixed import
from app.utils.limiters import limiter
from app.utils.cache_utils import cache_key_user_sessions, invalidate_user_sessions_cache, cache_key_user_single_session
import logging
from sqlalchemy.orm import joinedload

study_sessions_bp = Blueprint("sessions", "sessions", url_prefix="/sessions")


@study_sessions_bp.route("")
class StudySessionListCreate(MethodView):
    @jwt_required()
    @study_sessions_bp.arguments(StudySessionsSchema)
    @study_sessions_bp.response(201)
    @limiter.limit("20 per minute")
    def post(self, session_data):
        """Create a new session for the subject for the current user"""
        current_user_id = int(get_jwt_identity())

        # Extract subject_id from the payload
        subject_id = session_data["subject_id"]

        # Verify subject belongs to the user
        subject = Subject.query.filter_by(id=subject_id, user_id=current_user_id).first()
        if not subject:
            logging.error(f"The subject '{subject}' was not found in the database or it's unauthorized.")
            return {"error": "Subject not found or unauthorized"}, 403

        
        start = session_data["start_time"]
        end = session_data["end_time"]
        duration = int((end - start).total_seconds() // 60)

        new_session = StudySessions(
            start_time=start,
            end_time=end,
            duration_minutes=duration,
            subject_id=subject_id,
            notes=session_data.get("notes", None)
        )

        db.session.add(new_session)
        db.session.commit()

        invalidate_user_sessions_cache()
        logging.info("Study session was added successfully.")
        return {
            "message": "Session added successfully",
            "id": new_session.id,
            "subject_id": new_session.subject_id
        }, 201

    @jwt_required()
    @limiter.limit("100 per minute")
    def get(self):
        """Get all sessions for the current subject"""
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 10, type=int), 100)        
        # Generate cache key
        cache_key = cache_key_user_sessions(page, per_page)
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logging.info(f"Cache HIT for sessions (user {current_user_id}, page {page})")
            return cached_result, 200
        
        logging.info(f"Cache MISS for sessions (user {current_user_id}, page {page})")
        
        user_subjects = Subject.query.filter_by(user_id=current_user_id).all()
        subject_ids = [s.id for s in user_subjects]

        sessions = (
            db.session.query(StudySessions)
            .options(joinedload(StudySessions.subject))   
            .filter(StudySessions.subject_id.in_(subject_ids))
            .paginate(page=page, per_page=per_page, error_out=False)
        )

        result = {
            "sessions": [
                {
                    "session_id": ses.id,
                    "subject_id": ses.subject_id,
                    "subject_name": ses.subject.name,
                    "start_time": ses.start_time.isoformat() if ses.start_time else None,
                    "end_time": ses.end_time.isoformat() if ses.end_time else None,
                    "duration_minutes": ses.duration_minutes,
                    "notes": ses.notes
                }
                for ses in sessions.items
            ],
            "total": sessions.total,
            "page": sessions.page,
            "pages": sessions.pages
        }
        
        # Store in cache for 5 minutes
        cache.set(cache_key, result, timeout=300)
        
        return result, 200

    
@study_sessions_bp.route("/<int:id>")
class StudySessionDetail(MethodView):
    @jwt_required()
    @limiter.limit("100 per minute")
    def get(self,id):
        """Get a single session for the current subject"""
        current_user_id = int(get_jwt_identity())
        
        # Generate cache key
        cache_key = cache_key_user_single_session(id)
        
        # Try to get from cache
        cached_result = cache.get(cache_key)
        if cached_result:
            logging.info(f"Cache HIT for sessions (user {current_user_id}, session {id})")
            return cached_result, 200
        
        logging.info(f"Cache MISS for sessions (user {current_user_id}, session {id})")
        
        session = (
            db.session.query(StudySessions)
            .options(joinedload(StudySessions.subject))
            .join(Subject)
            .filter(StudySessions.id == id, Subject.user_id == current_user_id)
            .first()
        )

        if not session:
            return {"error": "Study session not found"}, 404

        result = {
            "session_id": session.id,
            "subject_id": session.subject_id,
            "subject_name": session.subject.name,
            "start_time": session.start_time.isoformat() if session.start_time else None,
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "duration_minutes": session.duration_minutes,
            "notes": session.notes
        }

        cache.set(cache_key, result, timeout=300)

        return result, 200
    
    @jwt_required()
    @study_sessions_bp.arguments(EditStudySessionsSchema)
    @study_sessions_bp.response(200)
    @limiter.limit("20 per minute")
    def put(self, session_data, id):
        """Update a study session"""
        current_user_id = int(get_jwt_identity())

        session = StudySessions.query.get(id)
        if not session:
            logging.error("Session was not found in the database.")
            return {"error": "Session not found"}, 404

        subject = Subject.query.filter_by(
            id=session.subject_id,
            user_id=current_user_id
        ).first()

        if not subject:
            logging.error("Unauthorized attempt to update session.")
            return {"error": "Unauthorized"}, 403
        
        start = session_data["start_time"]
        end = session_data["end_time"]
        duration = int((end - start).total_seconds() // 60)

        session.start_time = start
        session.end_time = end
        session.duration_minutes = duration
        session.notes = session_data.get("notes", None)
        db.session.commit()

        invalidate_user_sessions_cache()
        logging.info(f"Session with id {id} updated successfully.")
        return {"message": "Session updated successfully"}, 200
    
    @jwt_required()
    @limiter.limit("20 per minute")
    def delete(self, id):
        current_user_id = int(get_jwt_identity())

        session = StudySessions.query.get(id)
        if not session:
            logging.error("Session was not found in the database.")
            return {"error": "Session not found"}, 404
        
        subject = Subject.query.filter_by(
            id=session.subject_id,
            user_id=current_user_id
        ).first()

        if not subject:
            return {"error": "Unauthorized"}, 403
        
        db.session.delete(session)
        db.session.commit()
        invalidate_user_sessions_cache()
        logging.info("Session was deleted succesfully.")
        return {"message": "Session deleted"}, 200
