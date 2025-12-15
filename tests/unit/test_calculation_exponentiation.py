import pytest
from app.models.calculation import Exponentiation

def test_exponentiation_basic():
    calc = Exponentiation(user_id=None, inputs=[2, 3])
    assert calc.get_result() == 8

def test_exponentiation_zero_exponent():
    calc = Exponentiation(user_id=None, inputs=[5, 0])
    assert calc.get_result() == 1

def test_exponentiation_negative_exponent():
    calc = Exponentiation(user_id=None, inputs=[2, -2])
    assert calc.get_result() == 0.25

def test_exponentiation_invalid_inputs():
    calc = Exponentiation(user_id=None, inputs=[2])
    with pytest.raises(ValueError):
        calc.get_result()
    calc = Exponentiation(user_id=None, inputs=[2, 3, 4])
    with pytest.raises(ValueError):
        calc.get_result()
