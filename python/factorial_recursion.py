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
    if n == 1:
        logging.debug('n = 1, returning ')
        return 1
    else:
        logging.debug('n = %d, returning factorial(%d) ' % (n, n - 1))
        return n * factorial(n - 1)

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    if args.number < 0:
        logging.error('Cannot calculate factorial of a negative number!')
        raise ValueError('Invalid value %d - n must be positive' % n)

    answer = factorial(args.number)
    print('%d! = %d' % (args.number, answer))
