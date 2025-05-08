#!/usr/bin/env python3

"""
Calculates the factorial of a non-negative integer. The algorithm uses a for-loop.
"""

import argparse
import logging



def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('number', type=int)
    parser.add_argument('-q', '--quiet', help='Quiet mode', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    return parser.parse_args()


def configure_logging(args):
    log_level = logging.INFO
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')


def factorial(n):
    if n < 0:
        logging.error('Cannot calculate factorial of a negative number!')
        raise ValueError('Invalid value %d - n must be positive' % n)

    result = 1
    for i in range(1, n + 1):
        result *= i
        logging.debug('Calculated factorial of %d: %d' % (i, result))

    return result


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    answer = factorial(args.number)
    print('Result = %d' % answer)
