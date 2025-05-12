#!/usr/bin/env python3

import argparse
import logging
from linecache import cache

"""
Calculates the minimum number of people needed to achieve a better-than-evens chance
of two sharing a birthday. Assumes that birthdays are uniformly distributed over
a 365-day year. 
"""

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
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

def calculate_birthdays(args):
    return 365

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    people = calculate_birthdays(args)
    print('%d people are needed for a better-than-evens chance of 2 sharing a birthday' % people)