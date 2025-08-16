#!/usr/bin/env python3

import pytest

import concept2_erg_stats

def test_exact_minute_split_to_seconds():
    split = "2:00"
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_exact_minute_single_seconds_split_to_seconds():
    split = "2:0"
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_exact_decimal_point_split_to_seconds():
    split = "2:00.0"
    expected_value = 120
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_typical_split_to_seconds():
    split = "1:45"
    expected_value = 105
    assert concept2_erg_stats.convert_split_to_seconds(split) == expected_value

def test_split_too_low():
    split = "0:59"
    with pytest.raises(ValueError):
        concept2_erg_stats.convert_split_to_seconds(split)

def test_split_too_high():
    split = "4:01"
    with pytest.raises(ValueError):
        concept2_erg_stats.convert_split_to_seconds(split)

