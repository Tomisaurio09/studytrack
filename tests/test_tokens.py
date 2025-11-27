from flask_jwt_extended import create_access_token, decode_token

def test_jwt_token_creation(app):
    with app.app_context():
        token = create_access_token(identity="5")
        decoded = decode_token(token)

        assert decoded["sub"] == "5"        
        assert "exp" in decoded          

def test_jwt_settings(app):
    with app.app_context():
        token = create_access_token(identity="5")
        decoded = decode_token(token)

        assert decoded["type"] == "access"
