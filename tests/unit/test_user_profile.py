import pytest
from app.models.user import User

class DummyUser:
    def __init__(self, password):
        self.password = User.hash_password(password)
    
    def verify_password(self, plain):
        return User.verify_password(self, plain)
    
    def update(self, **kwargs):
        """Update user attributes with provided keyword arguments."""
        for key, value in kwargs.items():
            setattr(self, key, value)

def test_hash_and_verify_password():
    user = DummyUser("TestPass123!")
    assert user.verify_password("TestPass123!")
    assert not user.verify_password("WrongPass")

def test_update_user_fields():
    user = DummyUser("TestPass123!")
    user.first_name = "Alice"
    user.last_name = "Smith"
    user.email = "alice@example.com"
    user.username = "alicesmith"
    user.update(first_name="Bob", email="bob@example.com")
    assert user.first_name == "Bob"
    assert user.email == "bob@example.com"
    assert user.last_name == "Smith"
    assert user.username == "alicesmith"

def test_password_change():
    user = DummyUser("OldPass123!")
    old_hash = user.password
    new_hash = User.hash_password("NewPass123!")
    user.password = new_hash
    assert user.verify_password("NewPass123!")
    assert not user.verify_password("OldPass123!")
    assert user.password != old_hash
