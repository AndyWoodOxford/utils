#!/usr/bin/env python3

"""
Tabulates 2K and 5K times for a list of 500m splits. The high and low splits are entered using
the format 'm:ss' or 'm:ss.x' and must both be between 1 and 4 minutes.
"""

import argparse
import logging
import re

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

def verify_split(split):
    print('SPLIT %s' % split)
    pattern = re.compile('^(\\d){1}:(\\d){1,2}$')
    if not re.match(pattern, split):
        print('FAILED MATCH')
        raise ValueError('The string "%s" is not a valid format for a split' % split)
    print('PASSED MATCH')
    minutes = int(split.split(':')[0])
    print('MINUTES %d' % minutes)
    if minutes < 1:
        print('TOO LOW')
        raise ValueError('The split of "%s" is too low' % split)
    elif minutes >=4:
        print('TOO HIGH')
        raise ValueError('The split of "%s" is too low' % split)
    print('VERIFY OK')

def convert_split_to_seconds(split):
    verify_split(split)
    logging.debug('Converting split %s into seconds.' % split)
    minutes = int(split.split(':')[0])
    seconds = float(split.split(':')[1])
    print('SECONDS ARE %.1f' % seconds)
    print('TOTAL %.1f seconds' % (minutes * 60 + seconds))
    return minutes * 60 + seconds

def tabulate_times(high_split, low_split, increment = 1.0):
    logging.debug('Tabulating times for splits between %s to %s in increments of %.1f second(s).' % (high_split, low_split, increment))
    start = convert_split_to_seconds(high_split)
    end = convert_split_to_seconds(low_split)

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)



    tabulate_times(HIGH_SPLIT, LOW_SPLIT)