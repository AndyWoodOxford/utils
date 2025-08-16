#!/usr/bin/env python3

"""
Tabulates 2K and 5K times for a list of 500m splits.
"""

import argparse
import logging
from fractions import Fraction

HIGH_SPLIT = "2:30"
LOW_SPLIT = "1:30"

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

    logging.basicConfig(level=log_level, format='%(levelname)s:%(message)s')

def convert_split_to_seconds(split):
    logging.debug('Converting split %s into seconds.' % split)
    return 0

def tabulate_times(high_split, low_split, increment = 1.0):
    logging.debug('Tabulating times for splits between %s to %s in increments of %.1f second(s).' % (high_split, low_split, increment))
    start = convert_split_to_seconds(high_split)
    end = convert_split_to_seconds(low_split)

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    tabulate_times(HIGH_SPLIT, LOW_SPLIT)