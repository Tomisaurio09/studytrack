from flask import jsonify
from flask_limiter.errors import RateLimitExceeded
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

def register_error_handlers(app):
    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(e):
        return jsonify({"error": "Database error", "details": str(e)}), 500

    @app.errorhandler(404)
    def not_found_error(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(RateLimitExceeded)
    def handle_rate_limit(e):
        return jsonify({"error": "Too Many Requests"}), 429

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        return jsonify({"errors": e.messages}), 400

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"error": "Method not allowed"}), 405

