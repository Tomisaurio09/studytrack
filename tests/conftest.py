# conftest.py
import pytest
from app import create_app, db
from app.models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    with app.app_context():
        user = User(
            username="tester",
            email="tester@example.com"
        )
        user.set_password("thomas12345")
        db.session.add(user)
        db.session.commit()
        return user.id

@pytest.fixture
def access_token(test_user, app):
    #test user es un user_id
    with app.app_context():
        return create_access_token(identity=str(test_user))

@pytest.fixture
def auth_headers(access_token):
    return {"Authorization": f"Bearer {access_token}"}
