"""Tests to improve model coverage."""

import pytest
import uuid
from app.models.calculation import Calculation, Addition, Subtraction, Multiplication, Division, Exponentiation

def test_calculation_factory_all_types():
    """Test calculation factory for all supported types."""
    user_id = uuid.uuid4()
    
    # Test all calculation types
    types_and_inputs = [
        ("addition", [1, 2, 3]),
        ("subtraction", [10, 3, 2]), 
        ("multiplication", [2, 3, 4]),
        ("division", [20, 4, 5]),
        ("exponentiation", [2, 8])
    ]
    
    for calc_type, inputs in types_and_inputs:
        calc = Calculation.create(calc_type, user_id, inputs)
        assert calc.type == calc_type
        assert calc.user_id == user_id
        assert calc.inputs == inputs

def test_calculation_get_result_not_implemented():
    """Test that base Calculation.get_result raises NotImplementedError."""
    user_id = uuid.uuid4()
    calc = Calculation(user_id=user_id, type="test", inputs=[1, 2])
    
    with pytest.raises(NotImplementedError):
        calc.get_result()

def test_calculation_repr():
    """Test calculation string representation."""
    user_id = uuid.uuid4()
    calc = Addition(user_id=user_id, inputs=[1, 2, 3])
    repr_str = repr(calc)
    
    assert "Calculation" in repr_str
    assert "addition" in repr_str  # type should be in repr
    assert "[1, 2, 3]" in repr_str  # inputs should be in repr

def test_calculation_validation_errors():
    """Test calculation validation for edge cases."""
    user_id = uuid.uuid4()
    
    # Test invalid inputs for each calculation type
    
    # Addition with invalid inputs
    add_calc = Addition(user_id=user_id, inputs="not a list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        add_calc.get_result()
    
    add_calc = Addition(user_id=user_id, inputs=[1])  # Too few inputs
    with pytest.raises(ValueError, match="at least two numbers"):
        add_calc.get_result()
    
    # Subtraction with invalid inputs
    sub_calc = Subtraction(user_id=user_id, inputs="not a list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        sub_calc.get_result()
    
    sub_calc = Subtraction(user_id=user_id, inputs=[5])  # Too few inputs
    with pytest.raises(ValueError, match="at least two numbers"):
        sub_calc.get_result()
    
    # Multiplication with invalid inputs
    mul_calc = Multiplication(user_id=user_id, inputs="not a list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        mul_calc.get_result()
    
    mul_calc = Multiplication(user_id=user_id, inputs=[3])  # Too few inputs
    with pytest.raises(ValueError, match="at least two numbers"):
        mul_calc.get_result()
    
    # Division with invalid inputs
    div_calc = Division(user_id=user_id, inputs="not a list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        div_calc.get_result()
    
    div_calc = Division(user_id=user_id, inputs=[8])  # Too few inputs
    with pytest.raises(ValueError, match="at least two numbers"):
        div_calc.get_result()
    
    # Division by zero
    div_calc = Division(user_id=user_id, inputs=[10, 0])
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        div_calc.get_result()
    
    # Exponentiation with invalid inputs
    exp_calc = Exponentiation(user_id=user_id, inputs="not a list")
    with pytest.raises(ValueError, match="Inputs must be a list"):
        exp_calc.get_result()
    
    exp_calc = Exponentiation(user_id=user_id, inputs=[2])  # Too few inputs
    with pytest.raises(ValueError, match="exactly two numbers"):
        exp_calc.get_result()
    
    exp_calc = Exponentiation(user_id=user_id, inputs=[2, 3, 4])  # Too many inputs
    with pytest.raises(ValueError, match="exactly two numbers"):
        exp_calc.get_result()

def test_calculation_factory_case_insensitive():
    """Test that calculation factory handles case variations."""
    user_id = uuid.uuid4()
    
    # Test uppercase
    calc = Calculation.create("ADDITION", user_id, [1, 2])
    assert calc.type == "addition"
    
    # Test mixed case
    calc = Calculation.create("Multiplication", user_id, [3, 4])
    assert calc.type == "multiplication"

def test_calculation_direct_instantiation():
    """Test direct instantiation of calculation subclasses."""
    user_id = uuid.uuid4()
    
    # Test direct instantiation and result calculation
    calc = Addition(user_id=user_id, inputs=[5, 10, 15])
    result = calc.get_result()
    assert result == 30
    
    calc = Subtraction(user_id=user_id, inputs=[20, 5, 3])
    result = calc.get_result()
    assert result == 12
    
    calc = Multiplication(user_id=user_id, inputs=[2, 3, 4])
    result = calc.get_result()
    assert result == 24
    
    calc = Division(user_id=user_id, inputs=[100, 5, 2])
    result = calc.get_result()
    assert result == 10.0
    
    calc = Exponentiation(user_id=user_id, inputs=[3, 3])
    result = calc.get_result()
    assert result == 27
