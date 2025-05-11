#!/usr/bin/env python3

"""
Calculates the factorial of a non-negative integer. The algorithm uses a for-loop.
"""

import argparse



def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('number', type=int)
    return parser.parse_args()


def factorial(n):
    if n < 0:
        raise ValueError('Invalid value %d - n must be positive' % n)

    if n ==0:
        return 1
    elif n == 1:
        return 1
    else:
        return n * factorial(n - 1)

if __name__ == '__main__':
    args = parse_args()

    answer = factorial(args.number)
    print('%d! = %d' % (args.number, answer))
