#!/usr/bin/env python3

"""
Tabulates 2K and 5K times for a sequence of 500m split times. The formula is
Watts = 2.8/pace^3, where pace = split / 500m. (see https://www.concept2.co.uk/training/watts-calculator)
"""

import argparse
import logging
import re

SPLIT_DISTANCE = 500
DEFAULT_HIGH_SPLIT = "2:15"
DEFAULT_LOW_SPLIT = "1:45"
DEFAULT_SPLIT_INCREMENT = 1.0
DEFAULT_DISTANCES = '2000,5000'
SPLIT_REGEX = '^(\\d){1}:(\\d){1,2}(\\.)?(\\d)?$'

COLUMN_WIDTH = 13

def default_distances():
    return DEFAULT_DISTANCES

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
        nargs='?',
        help='High 500m split (i.e. slowest pace), enter as e.g. "2:15", "2:20.5" etc. [' + default_high_split() + ']',
        action='store',
        default=default_high_split()
    )
    parser.add_argument(
        '-I', '--split-increment',
        metavar='INCR',
        type=float,
        help = 'Split increment in seconds, enter as e.g. "1", "1.5" etc. Rounded to one decimal place. [' + str(default_split_increment()) + ']',
        action='store',
        default=default_split_increment()
    )
    parser.add_argument(
        '-L', '--low-split',
        metavar='SPLIT',
        help='Low 500m split (i.e. fastest pace), enter as e.g. "2:00", "1:50.5" etc. [' + default_low_split() + ']',
        action='store',
        default=default_low_split()
    )
    parser.add_argument(
        '-d', '--distances',
        metavar='DISTANCES',
        help='Coma-separated list of integral distances, e.g. "1000,2000,10000" [' + default_distances() + ']',
        action='store',
        default=default_distances()
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

def verify_distances(distances):
    compiled_pattern = re.compile('^(\\w+)(,\\s*\\w+)*$')
    if not re.match(compiled_pattern, distances):
        raise ValueError('The distances string "%s" is not a valid comma-separated string of integers' % distances)

    for distance in distances.split(','):
        if not distance.isnumeric():
            raise ValueError('The distance "%s" is not numeric' % distance)

def convert_split_to_seconds(split):
    logging.debug('Converting split %s into seconds.' % split)
    minutes = int(split.split(':')[0])
    seconds = float(split.split(':')[1])
    logging.debug('The split "%s" is %.1f seconds' % (split, (minutes * 60 + seconds)))
    return minutes * 60 + seconds

def convert_seconds_to_split(seconds):
    minutes, seconds = divmod(seconds, 60)
    return '%d:%04.1f' % (int(minutes), float(seconds))

def convert_split_to_watts(split_seconds):
    pace = split_seconds / SPLIT_DISTANCE
    logging.debug('A split of %0.1f seconds corresponds to a pace of %0.4fs/m' % (split_seconds, pace))

    watts = 2.8 / (pace ** 3)
    logging.debug('A split of %0.1f seconds corresponds to a wattage of %0.1fw' % (split_seconds, watts))

    return '%0.1f' % watts

def get_header(distances):
    # split column
    fmt_template = '%s'
    header_cols = ['Split'.center(COLUMN_WIDTH)]

    # distance column(s)
    for distance in distances:
        fmt_template += '%s'
        header = '%sm' % distance
        header_cols.append(header.center(COLUMN_WIDTH))

    # wattage column
    fmt_template += '%s'
    header_cols.append('Watts'.center(COLUMN_WIDTH))

    return fmt_template % tuple(header_cols)

def get_row(split_string, split_seconds, distances):
    # split column
    fmt_template = '%s'

    # distance column(s)
    time_strings = [split_string.center(COLUMN_WIDTH)]
    for distance in distances:
        time_seconds = split_seconds * (distance / SPLIT_DISTANCE)
        time_string = convert_seconds_to_split(time_seconds)
        time_strings.append(time_string.center(COLUMN_WIDTH))
        fmt_template += '%s'

    # wattage column
    fmt_template += '%s'
    watts = str(convert_split_to_watts(split_seconds)).center(COLUMN_WIDTH)

    fmt_values = tuple(time_strings + [watts])
    return fmt_template % fmt_values

def tabulate_times(high_split, low_split, increment, distances):
    logging.debug('Tabulating times for splits between %s and %s in increments of %.1f second(s).' % (high_split, low_split, increment))
    start = convert_split_to_seconds(high_split)
    end = convert_split_to_seconds(low_split)

    if start <= end:
        raise ValueError('The "high" split must be greater than the "low" split')

    tabulation = [get_header(distances)]
    split_seconds = start
    while split_seconds >= end:
        split_string = convert_seconds_to_split(split_seconds)
        logging.debug('Calculating stats for %.1f seconds / %s split' % (split_seconds, split_string))
        tabulation.append(get_row(split_string, split_seconds, distances))
        split_seconds -= increment

    return '\n'.join(tabulation)

if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    verify_split(args.high_split, SPLIT_REGEX)
    verify_split(args.low_split, SPLIT_REGEX)
    verify_increment(args.split_increment)
    verify_distances(args.distances)

    dists_str = args.distances.split(',')
    dists_int = [int(d) for d in dists_str]

    output = tabulate_times(args.high_split, args.low_split, round(args.split_increment, 1), sorted(dists_int))
    print(output)