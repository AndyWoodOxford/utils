#!/usr/bin/env python3

import pytest

import concept2_erg_stats

def test_invalid_split():
    split = ''
    with pytest.raises(ValueError):
        concept2_erg_stats.verify_split(split, concept2_erg_stats.SPLIT_REGEX)

def test_invalid_split_missing_seconds():
    split = '2'
    with pytest.raises(ValueError):
        concept2_erg_stats.verify_split(split, concept2_erg_stats.SPLIT_REGEX)

def test_invalid_split_decimal_places():
    split = '2:00.123'
    with pytest.raises(ValueError):
        concept2_erg_stats.verify_split(split, concept2_erg_stats.SPLIT_REGEX)

def test_exact_minute_split_to_seconds():
    split = '2:00'
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_exact_minute_seconds_to_split():
    seconds = 120
    expected_value = '2:00.0'
    assert concept2_erg_stats.convert_seconds_to_split(seconds) == expected_value

def test_exact_minute_single_seconds_split_to_seconds():
    split = '2:0'
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_exact_decimal_point_split_to_seconds():
    split = '2:00.0'
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_exact_decimal_point_seconds_to_split():
    seconds = 120.0
    expected_value = '2:00.0'
    assert concept2_erg_stats.convert_seconds_to_split(seconds) == expected_value

def test_typical_split_to_seconds():
    split = '1:45'
    expected_value = 105
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_decimal_point_split_to_seconds():
    split = "1:50.5"
    expected_value = 110.5
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_decimal_point_seconds_to_split():
    seconds = 110.5
    expected_value = '1:50.5'
    assert concept2_erg_stats.convert_seconds_to_split(seconds) == expected_value

def test_invalid_increment():
    increment = 0.05
    with pytest.raises(ValueError):
        concept2_erg_stats.verify_increment(increment)

# Ref. https://www.concept2.co.uk/training/watts-calculator
def test_watts_normal_split():
    split = '2:00'
    expected_value = 202.5
    assert concept2_erg_stats.convert_split_to_watts(split) == expected_value

def test_watts_low_split():
    split = '1:30.0'
    expected_value = 480.1
    assert concept2_erg_stats.convert_split_to_watts(split) == expected_value