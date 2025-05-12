#!/usr/bin/env python3
import pytest

import prime_factors

def test_prime():
    n = 7
    assert prime_factors.is_prime(n)

def test_non_prime():
    n = 51
    assert not prime_factors.is_prime(n)
