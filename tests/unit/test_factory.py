import pytest
from app.factory import CalculationFactory


def test_compute_add():
    assert CalculationFactory.compute('Add', 2, 3) == 5


def test_compute_sub():
    assert CalculationFactory.compute('Sub', 5, 2) == 3


def test_compute_mul():
    assert CalculationFactory.compute('Multiply', 3, 4) == 12


def test_compute_div():
    assert CalculationFactory.compute('Divide', 10, 2) == 5


def test_compute_div_zero():
    with pytest.raises(ValueError):
        CalculationFactory.compute('Divide', 1, 0)


def test_compute_invalid():
    with pytest.raises(ValueError):
        CalculationFactory.compute('Unknown', 1, 2)
