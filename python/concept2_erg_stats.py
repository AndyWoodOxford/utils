#!/usr/bin/env python3

"""
Tabulates 2K and 5K times for a list of 500m splits. The high and low splits are entered using
the format 'm:ss' or 'm:ss.x' and must both be between 1 and 4 minutes.
"""

import argparse
import logging
import re

HIGH_SPLIT = "2:01"
LOW_SPLIT = "1:50"

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
    pattern = re.compile('^(\\d){1}:(\\d){1,2}(\\.)?(\\d)?$')
    if not re.match(pattern, split):
        raise ValueError('The string "%s" is not a valid format for a split' % split)
    minutes = int(split.split(':')[0])
    if minutes < 1:
        raise ValueError('The split of "%s" is too low' % split)
    elif minutes >=4:
        raise ValueError('The split of "%s" is too low' % split)

def convert_split_to_seconds(split):
    verify_split(split)
    logging.debug('Converting split %s into seconds.' % split)
    minutes = int(split.split(':')[0])
    seconds = float(split.split(':')[1])
    logging.debug('The split "%s" is %.1f seconds' % (split, (minutes * 60 + seconds)))
    return minutes * 60 + seconds

def convert_seconds_to_split(seconds):
    minutes, seconds = divmod(seconds, 60)
    return '%s:%s' % (int(minutes), float(seconds))

def tabulate_times(high_split, low_split, increment = 1.0):
    logging.debug('Tabulating times for splits between %s and %s in increments of %.1f second(s).' % (high_split, low_split, increment))
    start = convert_split_to_seconds(high_split)
    end = convert_split_to_seconds(low_split)

    split_seconds = start
    while split_seconds >= end:
        split_string = convert_seconds_to_split(split_seconds)
        print('SPLIT %.1f / %s' % (split_seconds, split_string))
        split_seconds -= increment

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)



    tabulate_times(HIGH_SPLIT, LOW_SPLIT)