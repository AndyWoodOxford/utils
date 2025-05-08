#!/usr/bin/env python3

"""
Calculates the factorial of a non-negative integer. The initial implementation
is hard-wired to a fixed integer. The algorithm uses a for-loop.
"""

import argparse
import logging

N = 5

def args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-q', '--quiet', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()

def factorial(n):
    if n < 0:
        raise ValueError('Invalid value %d - n must be positive' % n)

    result = 1
    for i in range(1, n + 1):
        result *= i

    return result

if __name__ == '__main__':
    args = args()
    answer = factorial(N)
    print('Result = %d' % answer)