#!/usr/bin/env python3

"""
Outputs the prime factors of a positive integer.
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


def prime_factors(number):
    return 1


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    answer = prime_factors(args.number)
    print('%d! = %d' % (args.number, answer))
