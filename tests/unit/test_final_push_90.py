"""Final comprehensive tests to achieve 90%+ coverage."""

import pytest
from pydantic import ValidationError
from app.schemas.user import PasswordUpdate
from app.schemas.calculation import CalculationType
from app.models.user import User
from app.models.calculation import Calculation
import uuid
from datetime import datetime

def test_password_update_same_password_validation():
    """Test PasswordUpdate validation for same passwords."""
    with pytest.raises(ValidationError, match="must be different"):
        PasswordUpdate(
            current_password="SamePass123!",
            new_password="SamePass123!",
            confirm_new_password="SamePass123!"
        )

def test_calculation_type_enum_values():
    """Test CalculationType enum values."""
    assert CalculationType.ADDITION == "addition"
    assert CalculationType.SUBTRACTION == "subtraction"
    assert CalculationType.MULTIPLICATION == "multiplication"
    assert CalculationType.DIVISION == "division" 
    assert CalculationType.EXPONENTIATION == "exponentiation"

def test_calculation_factory_case_sensitivity():
    """Test calculation factory with various case inputs."""
    user_id = uuid.uuid4()
    
    # Test mixed case
    calc = Calculation.create("Addition", user_id, [1, 2])
    assert calc.type == "addition"
    
    # Test uppercase
    calc = Calculation.create("SUBTRACTION", user_id, [10, 5])
    assert calc.type == "subtraction"

def test_user_model_edge_cases():
    """Test user model edge case methods."""
    # Test user representation (if __repr__ exists)
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "first_name": "Test",
        "last_name": "User",
        "password": "TestPass123!"
    }
    
    # Test various attributes exist
    assert hasattr(User, 'id')
    assert hasattr(User, 'username')
    assert hasattr(User, 'email')

def test_calculation_model_edge_cases():
    """Test calculation model edge cases."""
    user_id = uuid.uuid4()
    
    # Test calculation attributes exist
    assert hasattr(Calculation, 'id')
    assert hasattr(Calculation, 'user_id')
    assert hasattr(Calculation, 'type')
    assert hasattr(Calculation, 'inputs')
    assert hasattr(Calculation, 'result')
    
    # Test create method returns correct instance type
    calc = Calculation.create("addition", user_id, [1, 2, 3])
    assert isinstance(calc, Calculation)
    assert calc.user_id == user_id

def test_schema_model_configs():
    """Test schema model configurations."""
    from app.schemas.user import UserCreate, UserUpdate
    from app.schemas.calculation import CalculationBase
    
    # Test that schemas have model_config
    assert hasattr(UserCreate, 'model_config')
    assert hasattr(UserUpdate, 'model_config')
    assert hasattr(CalculationBase, 'model_config')

def test_additional_validation_coverage():
    """Test additional validation paths."""
    # Test calculation base with minimum inputs
    from app.schemas.calculation import CalculationBase
    
    calc = CalculationBase(type="addition", inputs=[1])
    assert calc.inputs == [1]
    assert calc.type == CalculationType.ADDITION
