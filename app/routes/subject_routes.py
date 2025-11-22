from flask import request, jsonify
from app.models import Subject
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.subject_schema import SubjectSchema, EditSubjectSchema  # Fixed import
from datetime import datetime, timezone
from app.utils.limiters import limiter
import logging
subject_bp = Blueprint("subject", "subject", url_prefix="/subjects")


@subject_bp.route("")
class SubjectListCreate(MethodView):
    @jwt_required()
    @subject_bp.arguments(SubjectSchema)
    @subject_bp.response(201)
    @limiter.limit("70 per hour")
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
        logging.info(f"New subject with id {new_subject.id} was created successfully.")
        return {
            "message": "Subject added successfully",
            "id": new_subject.id,
            "name": new_subject.name
        }, 201

    @jwt_required()
    @limiter.limit("60 per hour")
    def get(self):
        """Get all subjects for the current user"""
        current_user_id = int(get_jwt_identity())
        subjects = Subject.query.filter_by(user_id=current_user_id).all()
        result = [
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
            for s in subjects
        ]
        return result, 200


@subject_bp.route("/<int:id>")
class SubjectDetail(MethodView):
    @jwt_required()
    @subject_bp.arguments(EditSubjectSchema)
    @subject_bp.response(200)
    @limiter.limit("70 per hour") 
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
        logging.info(f"Subject with id {id} updated successfully.")
        return {"message": "Subject updated successfully"}, 200

    @jwt_required()
    @limiter.limit("50 per hour")
    def delete(self, id):
        """Delete a subject (only owner can delete)"""
        current_user_id = int(get_jwt_identity())

        subject = Subject.query.filter_by(id=id, user_id=current_user_id).first()
        if not subject:
            logging.error("Subject was not found in the database.")
            return {"error": "Subject not found or unauthorized"}, 404

        db.session.delete(subject)
        db.session.commit()
        logging.info("Subject was deleted succesfully.")
        return {"message": "Subject deleted successfully"}, 200