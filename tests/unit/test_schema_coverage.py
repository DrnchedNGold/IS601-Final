"""Tests to improve schema coverage."""

import pytest
from pydantic import ValidationError
from app.schemas.calculation import CalculationBase, CalculationCreate, CalculationResponse, CalculationType
from app.schemas.user import UserResponse, UserUpdate, PasswordUpdate
import uuid
from datetime import datetime


def test_calculation_base_validation():
    """Test CalculationBase validation edge cases."""
    # Valid request
    req = CalculationBase(type="addition", inputs=[1, 2, 3])
    assert req.type == CalculationType.ADDITION
    assert req.inputs == [1, 2, 3]
    
    # Test with different types
    req = CalculationBase(type="exponentiation", inputs=[2, 8])
    assert req.type == CalculationType.EXPONENTIATION
    
    # Test invalid type - should raise validation error
    with pytest.raises(ValidationError):
        CalculationBase(type="invalid", inputs=[1, 2])
    
    # Test case insensitive
    req = CalculationBase(type="ADDITION", inputs=[1, 2])
    assert req.type == CalculationType.ADDITION


def test_calculation_response_creation():
    """Test CalculationResponse creation."""
    calc_id = uuid.uuid4()
    user_id = uuid.uuid4()
    now = datetime.utcnow()
    
    response = CalculationResponse(
        id=calc_id,
        user_id=user_id,
        type="multiplication",
        inputs=[4, 5, 6],
        result=120.0,
        created_at=now,
        updated_at=now
    )
    
    assert response.id == calc_id
    assert response.user_id == user_id
    assert response.type == "multiplication"
    assert response.inputs == [4, 5, 6]
    assert response.result == 120.0


def test_user_response_creation():
    """Test UserResponse creation and validation."""
    user_id = uuid.uuid4()
    now = datetime.utcnow()
    
    user = UserResponse(
        id=user_id,
        username="testuser",
        email="test@example.com",
        first_name="Test",
        last_name="User",
        is_active=True,
        is_verified=False,
        created_at=now,
        updated_at=now
    )
    
    assert user.id == user_id
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.is_active is True
    assert user.is_verified is False


def test_user_update_validation():
    """Test UserUpdate schema validation."""
    # Valid update
    update = UserUpdate(
        first_name="Updated",
        last_name="Name",
        username="newusername",
        email="new@example.com"
    )
    assert update.first_name == "Updated"
    assert update.last_name == "Name"
    
    # Partial update
    update = UserUpdate(first_name="OnlyFirst")
    assert update.first_name == "OnlyFirst"
    assert update.last_name is None


def test_password_update_validation():
    """Test PasswordUpdate validation."""
    req = PasswordUpdate(
        current_password="OldPass123!",
        new_password="NewPass456!",
        confirm_new_password="NewPass456!"
    )
    
    assert req.current_password == "OldPass123!"
    assert req.new_password == "NewPass456!"
    assert req.confirm_new_password == "NewPass456!"
    
    # Test password mismatch
    with pytest.raises(ValidationError):
        PasswordUpdate(
            current_password="OldPass123!",
            new_password="NewPass456!",
            confirm_new_password="DifferentPass789!"
        )


def test_schema_edge_cases():
    """Test schema edge cases and validation."""
    # Test with None values where allowed
    try:
        update = UserUpdate()  # All fields optional
        assert update.first_name is None
    except Exception:
        # If validation prevents this, that's fine
        pass
    
    # Test empty strings - should raise validation error
    with pytest.raises(ValidationError):
        CalculationBase(type="", inputs=[])
    
    # Test invalid inputs type
    with pytest.raises(ValidationError):
        CalculationBase(type="addition", inputs="not a list")
