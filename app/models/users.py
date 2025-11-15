#users with id, email, name, password
from app import db
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import jwt
from time import time
from ...run import app

class User(UserMixin,db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password) #it generates the hashed password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password) #it compares the hashed password to the one the user just wrote
    
    def get_reset_password_token(self,expires_in=600):
        return jwt.encode({"reset_password": self.id, "exp": time() + expires_in},
                    app.config["SECRET_KEY"], algorithm="HS256")
    
    @staticmethod
    def verify_reste_password_token(token):
        try:
            id = jwt.decode(token, app.config["SECRET_KEY"],
                            algorithms=["HS256"])["reset_password"]
        except:
            return
        return db.session.get(User, id)