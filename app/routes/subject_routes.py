from flask import request
from app.models import Subject
from app import db, cache
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.subject_schema import SubjectSchema, EditSubjectSchema  # Fixed import
from datetime import datetime, timezone
from app.utils.limiters import limiter
from app.utils.cache_utils import cache_key_user_subjects, invalidate_user_subjects_cache, cache_key_user_single_subject
import logging
subject_bp = Blueprint("subject", "subject", url_prefix="/subjects")


@subject_bp.route("")
class SubjectListCreate(MethodView):
    @jwt_required()
    @subject_bp.arguments(SubjectSchema)
    @subject_bp.response(201)
    @limiter.limit("20 per minute")
    def post(self, user_data):
        """Create a new subject for the current user"""
        current_user_id = int(get_jwt_identity())

        new_subject = Subject(
            name=user_data["name"],
            description=user_data["description"],
            total_hours_goal=user_data["total_hours_goal"],
            total_hours_completed=user_data["total_hours_completed"],
            priority_level=user_data["priority_level"],
            status=user_data["status"],
            user_id=current_user_id
        )

        db.session.add(new_subject)
        db.session.commit()
        invalidate_user_subjects_cache()

        logging.info(f"New subject with id {new_subject.id} was created successfully.")
        return {
            "message": "Subject added successfully",
            "id": new_subject.id,
            "name": new_subject.name
        }, 201

    @jwt_required()
    @limiter.limit("100 per minute")
    def get(self):
        """Get all subjects for the current user"""
        current_user_id = int(get_jwt_identity())
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        cache_key = cache_key_user_subjects(page, per_page)

        cached_result = cache.get(cache_key)
        if cached_result:
            logging.info(f"Cache HIT for subjects (user {current_user_id}, page {page})")
            return cached_result, 200
        
        logging.info(f"Cache MISS for subjects (user {current_user_id}, page {page})")
        #pagination object
        subjects = Subject.query.filter_by(user_id=current_user_id).paginate(page=page, per_page=per_page, error_out=False)
        result = {
            "subjects": [
                {
                    "id": s.id,
                    "name": s.name,
                    "description": s.description,
                    "total_hours_goal": s.total_hours_goal,
                    "total_hours_completed": s.total_hours_completed,
                    "priority_level": s.priority_level.value,
                    "status": s.status.value,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "updated_at": s.updated_at.isoformat() if s.updated_at else None,
                }
                for s in subjects.items
            ],
            "total": subjects.total,
            "page": subjects.page,
            "pages": subjects.pages
        }
        
        # Store in cache for 5 minutes
        cache.set(cache_key, result, timeout=300)
        
        return result, 200


@subject_bp.route("/<int:id>")
class SubjectDetail(MethodView):
    @jwt_required()
    @limiter.limit("100 per minute")
    def get(self, id):
        """Get a single subject for the current user"""
        current_user_id = int(get_jwt_identity())
        cache_key = cache_key_user_single_subject(id)

        cached_result = cache.get(cache_key)
        if cached_result:
            logging.info(f"Cache HIT for subjects (user {current_user_id}, subject {id})")
            return cached_result, 200
        
        logging.info(f"Cache MISS for subjects (user {current_user_id}, subject {id})")
        subject = Subject.query.filter_by(id=id,user_id=current_user_id).first()
        if not subject:
            return {"error": "Subject not found"}, 404

        result = {
            "id": subject.id,
            "name": subject.name,
            "description": subject.description,
            "total_hours_goal": subject.total_hours_goal,
            "total_hours_completed": subject.total_hours_completed,
            "priority_level": subject.priority_level.value,
            "status": subject.status.value,
            "created_at": subject.created_at.isoformat() if subject.created_at else None,
            "updated_at": subject.updated_at.isoformat() if subject.updated_at else None,
        }

        cache.set(cache_key, result, timeout=300)

        return result, 200
    
    @jwt_required()
    @subject_bp.arguments(EditSubjectSchema)
    @subject_bp.response(200)
    @limiter.limit("20 per minute") 
    def put(self, user_data, id):
        """Update a subject (only owner can update)"""
        current_user_id = int(get_jwt_identity())

        subject = Subject.query.filter_by(id=id, user_id=current_user_id).first()
        if not subject:
            logging.error("Subject was not found in the database.")
            return {"error": "Subject not found or unauthorized"}, 404

        # Update fields
        subject.name = user_data["name"]
        subject.description = user_data["description"]
        subject.total_hours_goal = user_data["total_hours_goal"]
        subject.total_hours_completed = user_data["total_hours_completed"]
        subject.priority_level = user_data["priority_level"]
        subject.status = user_data["status"]
        subject.updated_at = datetime.now(timezone.utc)

        db.session.commit()
        invalidate_user_subjects_cache()
        logging.info(f"Subject with id {id} updated successfully.")
        return {"message": "Subject updated successfully"}, 200

    @jwt_required()
    @limiter.limit("20 per minute")
    def delete(self, id):
        """Delete a subject (only owner can delete)"""
        current_user_id = int(get_jwt_identity())

        subject = Subject.query.filter_by(id=id, user_id=current_user_id).first()
        if not subject:
            logging.error("Subject was not found in the database.")
            return {"error": "Subject not found or unauthorized"}, 404

        db.session.delete(subject)
        db.session.commit()
        invalidate_user_subjects_cache()
        logging.info("Subject was deleted succesfully.")
        return {"message": "Subject deleted successfully"}, 200