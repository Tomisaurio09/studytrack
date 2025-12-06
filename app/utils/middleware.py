from flask import request
from werkzeug.exceptions import Forbidden

ALLOWED_HOSTS = {"localhost", "127.0.0.1", "api.studytrack.com","studytrack-90ww.onrender.com"}

def enforce_allowed_hosts(app):
    @app.before_request
    def _check_host():
        host = request.headers.get("Host", "").split(":")[0]
        if host not in ALLOWED_HOSTS:
            raise Forbidden(f"Host not allowed: {host}")
