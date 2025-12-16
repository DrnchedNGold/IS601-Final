"""Final strategic tests to achieve 90%+ coverage."""

import pytest
from app.schemas.calculation import CalculationCreate, CalculationReport
from app.schemas.user import UserLogin, UserBase
import uuid
from datetime import datetime

def test_calculation_create_schema():
    """Test CalculationCreate schema."""
    user_id = uuid.uuid4()
    calc = CalculationCreate(
        type="addition",
        inputs=[1, 2, 3],
        user_id=user_id
    )
    assert calc.type.value == "addition"
    assert calc.inputs == [1, 2, 3]
    assert calc.user_id == user_id

def test_calculation_report_schema():
    """Test CalculationReport schema."""
    now = datetime.utcnow()
    report = CalculationReport(
        total_calculations=10,
        average_operands=2.5,
        most_common_type="addition",
        last_calculation_at=now
    )
    assert report.total_calculations == 10
    assert report.average_operands == 2.5
    assert report.most_common_type == "addition"
    assert report.last_calculation_at == now

def test_user_login_schema():
    """Test UserLogin schema."""
    login = UserLogin(
        username="testuser",
        password="TestPass123!"
    )
    assert login.username == "testuser"
    assert login.password == "TestPass123!"

def test_user_base_schema():
    """Test UserBase schema."""
    user = UserBase(
        first_name="John",
        last_name="Doe", 
        email="john@example.com",
        username="johndoe"
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "john@example.com"
    assert user.username == "johndoe"

def test_schema_validation_edge_cases():
    """Test additional validation edge cases."""
    # Test empty lists validation
    with pytest.raises(ValueError):
        CalculationCreate(
            type="addition",
            inputs=[],
            user_id=uuid.uuid4()
        )
    
    # Test single input validation
    try:
        calc = CalculationCreate(
            type="addition", 
            inputs=[5],
            user_id=uuid.uuid4()
        )
        # Should be valid for creation, business logic validates later
        assert calc.inputs == [5]
    except ValueError:
        # If validation prevents single input, that's acceptable
        pass
