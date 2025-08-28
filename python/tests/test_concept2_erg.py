#!/usr/bin/env python3

import pytest

from Concept2Split import Split

def test_invalid_split():
    with pytest.raises(ValueError):
        split = Split.display('')

def test_invalid_split_missing_seconds():
    with pytest.raises(ValueError):
        split = Split.display('2')

def test_invalid_split_decimal_places():
    with pytest.raises(ValueError):
        split = Split.display('2:00.123')

def test_exact_minute_split_to_seconds():
    split = Split.display('2:00')
    expected_value = 120
    assert split.split == expected_value

def test_exact_minute_single_seconds_split_to_seconds():
    split = Split.display('2:00.0')
    expected_value = 120
    assert split.split == expected_value

def test_exact_minute_seconds_to_split():
    split = Split.seconds(120)
    expected_value = '2:00.0'
    assert split.split_display == expected_value

def test_typical_split_to_seconds():
    split = Split.display('1:45')
    expected_value = 105
    assert split.split == expected_value

def test_decimal_point_split_to_seconds():
    split = Split.display('1:50.5')
    expected_value = 110.5
    assert split.split == expected_value

def test_invalid_distance():
    distances = [500, -1]
    with pytest.raises(ValueError):
        split = Split.display('2:00', distances)

def test_non_integer_distance():
    distances = [1000, 'foo']
    with pytest.raises(ValueError):
        split = Split.display('2:00', distances)

# Ref. https://www.concept2.co.uk/training/watts-calculator
def test_watts_from_seconds():
    split = Split.seconds(120)
    expected_value = 202.5
    assert split.watts == expected_value

def test_watts_from_display():
    split = Split.display("1:45.0")
    expected_value = 302.3
    assert split.watts == expected_value
