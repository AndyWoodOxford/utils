#!/usr/bin/env python3
import pytest

import prime_factors

def test_prime():
    n = 7
    assert prime_factors.is_prime(n)

def test_non_prime():
    n = 51
    assert not prime_factors.is_prime(n)

def test_factoring_prime():
    n = 67
    factors = prime_factors.prime_factors(n)
    assert not factors

def test_factoring_distinct_factors():
    n = 255 # 3 * 5 * 17
    factors = prime_factors.prime_factors(n)
    assert len(factors) == 3
    assert 3 in factors and 5 in factors and 17 in factors

def test_factoring_nondistinct_factors():
    n = 45 # 3 * 3 * 5
    factors = prime_factors.prime_factors(n)
    assert factors.count(3) == 2 and  5 in factors

def test_factoring_exponent():
    n = 1024 # 2^10
    factors = prime_factors.prime_factors(n)
    assert len(factors) == 10 and factors.count(2) == 10
