#!/usr/bin/env python3

"""
Tabulates 2K and 5K times for a sequence of 500m split times.
"""

import argparse
import logging
import re

DEFAULT_HIGH_SPLIT = "2:15"
DEFAULT_LOW_SPLIT = "1:45"
DEFAULT_SPLIT_INCREMENT = 1

DISTANCES = [2000, 5000]

COLUMN_WIDTH = 13

def default_high_split():
    return DEFAULT_HIGH_SPLIT

def default_low_split():
    return DEFAULT_LOW_SPLIT

def default_split_increment():
    return DEFAULT_SPLIT_INCREMENT

def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '-H', '--high-split',
        metavar='SPLIT',
        help='High 500m split (i.e. slowest pace), enter as e.g. "2:15", "2:20.5" etc',
        action='store',
        default=default_high_split()
    )
    parser.add_argument(
        '-I', '--split-increment',
        metavar='INCR',
        type=float,
        help = 'Split increment in seconds, enter as e.g. "1", "1.5" etc. Rounded to one decimal place.',
        action='store',
        default=default_split_increment()
    )
    parser.add_argument(
        '-L', '--low-split',
        metavar='SPLIT',
        help='Low 500m split (i.e. fastest pace), enter as e.g. "2:00", "1:50.5" etc',
        action='store',
        default=default_low_split()
    )
    parser.add_argument(
        '-q', '--quiet',
        help='Quiet mode',
        action='store_true')
    parser.add_argument(
        '-v', '--verbose',
        help='Verbose mode',
        action='store_true')
    return parser.parse_args()


def configure_logging(args):
    log_level = logging.INFO
    if args.quiet:
        log_level = logging.WARNING
    elif args.verbose:
        log_level = logging.DEBUG

    logging.basicConfig(level=log_level, format='%(levelname)s:%(message)s')

def verify_split(split, pattern):
    compiled_pattern = re.compile(pattern)
    if not re.match(compiled_pattern, split):
        raise ValueError('The string "%s" is not a valid format for a split' % split)

def verify_increment(increment):
    if increment < 0.1:
        raise ValueError('The increment must be at least 0.1; %s is invalid' % str(increment))

def convert_split_to_seconds(split):
    logging.debug('Converting split %s into seconds.' % split)
    minutes = int(split.split(':')[0])
    seconds = float(split.split(':')[1])
    logging.debug('The split "%s" is %.1f seconds' % (split, (minutes * 60 + seconds)))
    return minutes * 60 + seconds

def convert_seconds_to_split(seconds):
    minutes, seconds = divmod(seconds, 60)
    return '%d:%04.1f' % (int(minutes), float(seconds))

def get_header():
    header_row = 'Split'.center(COLUMN_WIDTH) + '2K'.center(COLUMN_WIDTH) + '5K'.center(COLUMN_WIDTH)
    return '%s\n%s' % (header_row, '-' * len(header_row))

def get_row(split_string, split_seconds):
    fmt_template = '%s'  # for the split_string
    time_strings = [split_string.center(COLUMN_WIDTH)]
    for distance in DISTANCES:
        time_seconds = split_seconds * (distance / 500)
        time_string = convert_seconds_to_split(time_seconds)
        time_strings.append(time_string.center(COLUMN_WIDTH))
        fmt_template += '%s'

    fmt_values = tuple(time_strings)
    return fmt_template % fmt_values

def tabulate_times(high_split, low_split, increment):
    logging.debug('Tabulating times for splits between %s and %s in increments of %.1f second(s).' % (high_split, low_split, increment))
    start = convert_split_to_seconds(high_split)
    end = convert_split_to_seconds(low_split)

    if start <= end:
        raise ValueError('The "high" split must be greater than the "low" split')

    output = [get_header()]
    split_seconds = start
    while split_seconds >= end:
        split_string = convert_seconds_to_split(split_seconds)
        logging.debug('Calculating stats for %.1f seconds / %s split' % (split_seconds, split_string))
        output.append(get_row(split_string, split_seconds))
        split_seconds -= increment

    return '\n'.join(output)

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    verify_split(args.high_split, pattern = '^(\\d){1}:(\\d){1,2}(\\.)?(\\d)?$')
    verify_split(args.low_split, pattern = '^(\\d){1}:(\\d){1,2}(\\.)?(\\d)?$')
    verify_increment(args.split_increment)

    output = tabulate_times(args.high_split, args.low_split, round(args.split_increment, 1))
    print(output)