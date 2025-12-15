import pytest
from uuid import UUID
import pydantic_core
from sqlalchemy.exc import IntegrityError
from app.models.user import User

from app.auth import jwt as jwt_utils
from app.schemas.token import TokenType
from fastapi import HTTPException
from datetime import timedelta
import secrets

def test_password_hashing(db_session, fake_user_data):
    """Test password hashing and verification functionality"""
    original_password = "TestPass123"  # Use known password for test
    hashed = User.hash_password(original_password)
    
    user = User(
        first_name=fake_user_data['first_name'],
        last_name=fake_user_data['last_name'],
        email=fake_user_data['email'],
        username=fake_user_data['username'],
        password=hashed
    )
    
    assert user.verify_password(original_password) is True
    assert user.verify_password("WrongPass123") is False
    assert hashed != original_password

def test_jwt_verify_password_and_hash():
    """Directly test jwt.verify_password and get_password_hash"""
    password = "SuperSecret123"
    hashed = jwt_utils.get_password_hash(password)
    assert jwt_utils.verify_password(password, hashed)
    assert not jwt_utils.verify_password("WrongPassword", hashed)

def test_jwt_create_token_success():
    """Test create_token returns a valid JWT string"""
    user_id = "test-user-id"
    token = jwt_utils.create_token(user_id, TokenType.ACCESS)
    assert isinstance(token, str)
    assert token.count('.') == 2  # JWT format

def test_jwt_create_token_error(monkeypatch):
    """Test create_token error handling"""
    def bad_encode(*args, **kwargs):
        raise Exception("Encoding failed")
    monkeypatch.setattr(jwt_utils.jwt, "encode", bad_encode)
    with pytest.raises(HTTPException) as exc:
        jwt_utils.create_token("user", TokenType.ACCESS)
    assert "Could not create token" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_jwt_decode_token_valid(monkeypatch):
    """Test decode_token with valid token"""
    user_id = "decode-user"
    token = jwt_utils.create_token(user_id, TokenType.ACCESS)
    async def fake_is_blacklisted(jti):
        return False
    monkeypatch.setattr(jwt_utils, "is_blacklisted", fake_is_blacklisted)
    payload = await jwt_utils.decode_token(token, TokenType.ACCESS)
    assert payload["sub"] == user_id
    assert payload["type"] == TokenType.ACCESS.value

@pytest.mark.asyncio
async def test_jwt_decode_token_invalid_type(monkeypatch):
    """Test decode_token with wrong token type"""
    user_id = "decode-user"
    token = jwt_utils.create_token(user_id, TokenType.REFRESH)
    async def fake_is_blacklisted(jti):
        return False
    monkeypatch.setattr(jwt_utils, "is_blacklisted", fake_is_blacklisted)
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.decode_token(token, TokenType.ACCESS)
    assert "Could not validate credentials" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_jwt_decode_token_blacklisted(monkeypatch):
    """Test decode_token with blacklisted token"""
    user_id = "blacklisted-user"
    token = jwt_utils.create_token(user_id, TokenType.ACCESS)
    async def fake_is_blacklisted(jti):
        return True
    monkeypatch.setattr(jwt_utils, "is_blacklisted", fake_is_blacklisted)
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.decode_token(token, TokenType.ACCESS)
    assert "Token has been revoked" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_jwt_decode_token_expired(monkeypatch):
    """Test decode_token with expired token"""
    user_id = "expired-user"
    token = jwt_utils.create_token(
        user_id, TokenType.ACCESS, expires_delta=timedelta(seconds=-1)
    )
    monkeypatch.setattr(jwt_utils, "is_blacklisted", lambda jti: False)
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.decode_token(token, TokenType.ACCESS)
    assert "Token has expired" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_jwt_decode_token_invalid(monkeypatch):
    """Test decode_token with invalid token"""
    monkeypatch.setattr(jwt_utils, "is_blacklisted", lambda jti: False)
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.decode_token("invalid.token", TokenType.ACCESS)
    assert "Could not validate credentials" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_get_current_user_valid(monkeypatch):
    """Test get_current_user returns valid user"""
    class FakeUser:
        id = "user-id"
        is_active = True
    async def fake_decode_token(token, token_type):
        return {"sub": "user-id"}
    class FakeDB:
        def query(self, model):
            class Q:
                def filter(self, cond):
                    class F:
                        def first(self):
                            return FakeUser()
                    return F()
            return Q()
    monkeypatch.setattr(jwt_utils, "decode_token", fake_decode_token)
    db = FakeDB()
    user = await jwt_utils.get_current_user(token="token", db=db)
    assert user.id == "user-id"
    assert user.is_active

@pytest.mark.asyncio
async def test_get_current_user_not_found(monkeypatch):
    """Test get_current_user raises 404 if user not found"""
    async def fake_decode_token(token, token_type):
        return {"sub": "user-id"}
    class FakeDB:
        def query(self, model):
            class Q:
                def filter(self, cond):
                    class F:
                        def first(self):
                            return None
                    return F()
            return Q()
    monkeypatch.setattr(jwt_utils, "decode_token", fake_decode_token)
    db = FakeDB()
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.get_current_user(token="token", db=db)
    assert exc.value.status_code == 401
    assert "404" in str(exc.value.detail)
    assert "User not found" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_get_current_user_inactive(monkeypatch):
    """Test get_current_user raises 400 if user inactive"""
    class FakeUser:
        id = "user-id"
        is_active = False
    async def fake_decode_token(token, token_type):
        return {"sub": "user-id"}
    class FakeDB:
        def query(self, model):
            class Q:
                def filter(self, cond):
                    class F:
                        def first(self):
                            return FakeUser()
                    return F()
            return Q()
    monkeypatch.setattr(jwt_utils, "decode_token", fake_decode_token)
    db = FakeDB()
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.get_current_user(token="token", db=db)
    assert exc.value.status_code == 401
    assert "400" in str(exc.value.detail)
    assert "Inactive user" in str(exc.value.detail)

@pytest.mark.asyncio
async def test_get_current_user_exception(monkeypatch):
    """Test get_current_user raises 401 on exception"""
    async def fake_decode_token(token, token_type):
        raise Exception("decode error")
    class FakeDB:
        def query(self, model):
            class Q:
                def filter(self, cond):
                    class F:
                        def first(self):
                            return None
                    return F()
            return Q()
    monkeypatch.setattr(jwt_utils, "decode_token", fake_decode_token)
    db = FakeDB()
    with pytest.raises(HTTPException) as exc:
        await jwt_utils.get_current_user(token="token", db=db)
    assert exc.value.status_code == 401
    assert "decode error" in str(exc.value.detail)

# Existing tests below...

def test_user_registration(db_session, fake_user_data):
    """Test user registration process"""
    fake_user_data['password'] = "TestPass123"
    
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    assert user.first_name == fake_user_data['first_name']
    assert user.last_name == fake_user_data['last_name']
    assert user.email == fake_user_data['email']
    assert user.username == fake_user_data['username']
    assert user.is_active is True
    assert user.is_verified is False
    assert user.verify_password("TestPass123") is True

def test_duplicate_user_registration(db_session):
    """Test registration with duplicate email/username"""
    # First user data
    user1_data = {
        "first_name": "Test",
        "last_name": "User1",
        "email": "unique.test@example.com",
        "username": "uniqueuser1",
        "password": "TestPass123"
    }
    
    # Second user data with same email
    user2_data = {
        "first_name": "Test",
        "last_name": "User2",
        "email": "unique.test@example.com",  # Same email
        "username": "uniqueuser2",
        "password": "TestPass123"
    }
    
    # Register first user
    first_user = User.register(db_session, user1_data)
    db_session.commit()
    db_session.refresh(first_user)
    
    # Try to register second user with same email
    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2_data)

def test_user_authentication(db_session, fake_user_data):
    """Test user authentication and token generation"""
    # Use fake_user_data from fixture
    fake_user_data['password'] = "TestPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Test successful authentication
    auth_result = User.authenticate(
        db_session,
        fake_user_data['username'],
        "TestPass123"
    )
    
    assert auth_result is not None
    assert "access_token" in auth_result
    assert "token_type" in auth_result
    assert auth_result["token_type"] == "bearer"
    assert "user" in auth_result

def test_user_last_login_update(db_session, fake_user_data):
    """Test that last_login is updated on authentication"""
    fake_user_data['password'] = "TestPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Authenticate and check last_login
    assert user.last_login is None
    auth_result = User.authenticate(db_session, fake_user_data['username'], "TestPass123")
    db_session.refresh(user)
    assert user.last_login is not None

def test_unique_email_username(db_session):
    """Test uniqueness constraints for email and username"""
    # Create first user with specific test data
    user1_data = {
        "first_name": "Test",
        "last_name": "User1",
        "email": "unique_test@example.com",
        "username": "uniqueuser",
        "password": "TestPass123"
    }
    
    # Register and commit first user
    User.register(db_session, user1_data)
    db_session.commit()
    
    # Try to create user with same email
    user2_data = {
        "first_name": "Test",
        "last_name": "User2",
        "email": "unique_test@example.com",  # Same email
        "username": "differentuser",
        "password": "TestPass123"
    }
    
    with pytest.raises(ValueError, match="Username or email already exists"):
        User.register(db_session, user2_data)

def test_short_password_registration(db_session):
    """Test that registration fails with a short password"""
    # Prepare test data with a 5-character password
    test_data = {
        "first_name": "Password",
        "last_name": "Test",
        "email": "short.pass@example.com",
        "username": "shortpass",
        "password": "Shor1"  # 5 characters, should fail
    }
    
    # Attempt registration with short password
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        User.register(db_session, test_data)

def test_invalid_token():
    """Test that invalid tokens are rejected"""
    invalid_token = "invalid.token.string"
    result = User.verify_token(invalid_token)
    assert result is None

def test_token_creation_and_verification(db_session, fake_user_data):
    """Test token creation and verification"""
    fake_user_data['password'] = "TestPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Create token
    token = User.create_access_token({"sub": str(user.id)})
    
    # Verify token
    decoded_user_id = User.verify_token(token)
    assert decoded_user_id == user.id

def test_authenticate_with_email(db_session, fake_user_data):
    """Test authentication using email instead of username"""
    fake_user_data['password'] = "TestPass123"
    user = User.register(db_session, fake_user_data)
    db_session.commit()
    
    # Test authentication with email
    auth_result = User.authenticate(
        db_session,
        fake_user_data['email'],  # Using email instead of username
        "TestPass123"
    )
    
    assert auth_result is not None
    assert "access_token" in auth_result

def test_user_model_representation(test_user):
    """Test the string representation of User model"""
    expected = f"<User(name={test_user.first_name} {test_user.last_name}, email={test_user.email})>"
    assert str(test_user) == expected

def test_missing_password_registration(db_session):
    """Test that registration fails when no password is provided."""
    test_data = {
        "first_name": "NoPassword",
        "last_name": "Test",
        "email": "no.password@example.com",
        "username": "nopassworduser",
        # Password is missing
    }
    
    # Adjust the expected error message
    with pytest.raises(ValueError, match="Password must be at least 6 characters long"):
        User.register(db_session, test_data)
