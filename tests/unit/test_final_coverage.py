"""Final coverage boost tests to reach 90%+."""

import pytest
from pydantic import ValidationError
from app.schemas.user import UserCreate
from app.schemas.calculation import CalculationUpdate

def test_user_create_password_validation():
    """Test UserCreate password validation edge cases."""
    # Test password mismatch
    with pytest.raises(ValidationError, match="Passwords do not match"):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="ValidPass123!",
            confirm_password="DifferentPass456!"
        )
    
    # Test weak password - no uppercase
    with pytest.raises(ValidationError, match="uppercase letter"):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="weakpass123!",
            confirm_password="weakpass123!"
        )
    
    # Test weak password - no lowercase
    with pytest.raises(ValidationError, match="lowercase letter"):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="WEAKPASS123!",
            confirm_password="WEAKPASS123!"
        )
    
    # Test weak password - no digit
    with pytest.raises(ValidationError, match="digit"):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="WeakPass!",
            confirm_password="WeakPass!"
        )
    
    # Test weak password - no special character
    with pytest.raises(ValidationError, match="special character"):
        UserCreate(
            first_name="Test",
            last_name="User",
            email="test@example.com",
            username="testuser",
            password="WeakPass123",
            confirm_password="WeakPass123"
        )

def test_calculation_update_validation():
    """Test CalculationUpdate validation."""
    # Valid update
    update = CalculationUpdate(inputs=[10, 20, 30])
    assert update.inputs == [10, 20, 30]
    
    # Update with None (optional)
    update = CalculationUpdate()
    assert update.inputs is None
    
    # Test too few inputs - should raise validation error about minimum items
    with pytest.raises(ValidationError):
        CalculationUpdate(inputs=[5])

def test_validation_edge_cases():
    """Test various validation edge cases."""
    # Test empty inputs list
    with pytest.raises(ValidationError):
        CalculationUpdate(inputs=[])

def test_additional_user_validations():
    """Test additional user validation paths."""
    # Test valid user creation
    user = UserCreate(
        first_name="Valid",
        last_name="User",
        email="valid@example.com",
        username="validuser",
        password="ValidPass123!",
        confirm_password="ValidPass123!"
    )
    assert user.first_name == "Valid"
    assert user.password == "ValidPass123!"
    
    # Test short password
    with pytest.raises(ValidationError):
        UserCreate(
            first_name="Test",
            last_name="User", 
            email="test@example.com",
            username="testuser",
            password="short",
            confirm_password="short"
        )
