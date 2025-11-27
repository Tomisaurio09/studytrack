def test_check_hashing(user):
    password = "securepassword"
    user.set_password(password)
    assert user.check_password(password) is True
    assert user.check_password("wrongpassword") is False

