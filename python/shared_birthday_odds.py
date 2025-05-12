#!/usr/bin/env python3

import argparse
import logging
from fractions import Fraction

"""
Calculates the minimum number of people needed to achieve a better-than-evens chance
of two sharing a birthday. Assumes that birthdays are uniformly distributed over
a 365-day year. 
"""

PROBABILITY_THRESHOLD = 0.5

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

def calculate_birthdays():
    # Starting with the certainty of one person *not* sharing a birthday,
    # iteratively add people until the converse probability drops below
    # the threshold
    count = 1
    converse_probability = 1.0
    while converse_probability > PROBABILITY_THRESHOLD:
        f = Fraction(365 - (count - 1), 365)
        converse_probability *= float(f)
        logging.debug('%d people - %f probability of not sharing a birthday' % (count, converse_probability))

        count += 1

    return count - 1

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    people = calculate_birthdays()
    print('%d people are needed for a better-than-evens chance of 2 sharing a birthday' % people)