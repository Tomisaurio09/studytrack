from flask import request, jsonify
from app.models import StudySessions
from app import db
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask.views import MethodView
from app.schemas.study_sessions_schema import StudySessionsSchema # Fixed import
from datetime import datetime, timezone

study_sessions_bp = Blueprint("study_sessions", "study_sessions", url_prefix="/study_sessions")

#LOS 4 CRUD ENDPOINTS