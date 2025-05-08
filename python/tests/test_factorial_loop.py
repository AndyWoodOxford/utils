#!/usr/bin/env python3
import pytest

from factorial_loop import factorial

def test_small_factorial():
    n = 3
    expected_result = 6
    assert factorial(n) == expected_result

def test_factorial_zero():
    n = 0
    expected_result = 1
    assert factorial(n) == expected_result

def test_negative_factorial():
    n = -3
    with pytest.raises(ValueError):
        factorial(n)