#!/usr/bin/env python3
import pytest

import factorial_loop
import factorial_recursion


def test_small_factorial_loop():
    n = 3
    expected_result = 6
    assert factorial_loop.factorial(n) == expected_result

def test_factorial_zero_loop():
    n = 0
    expected_result = 1
    assert factorial_loop.factorial(n) == expected_result

def test_negative_factorial_loop():
    n = -3
    with pytest.raises(ValueError):
        factorial_loop.factorial(n)

def test_small_factorial_recursion():
    n = 3
    expected_result = 6
    assert factorial_recursion.factorial(n) == expected_result

def test_factorial_zero_recursion():
    n = 0
    expected_result = 1
    assert factorial_recursion.factorial(n) == expected_result

def test_negative_factorial_recursion():
    n = -3
    with pytest.raises(ValueError):
        factorial_recursion.factorial(n)