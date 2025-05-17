#!/usr/bin/env python3

import argparse
import logging
from fractions import Fraction

# An EVENT is a subset of all possible outcomes of an experiment, e.g. rolling an odd
# number on a (fair) die.
# A SIMPLE EVENT is one with a single outcome, e.g. rolling a 6 on a (fair) die.
# A PROBABILITY of an event is the likelihood of it happening and is a number between 0
# (the event cannot happen) and 1 (the event is certain to happen).
# The sum of the probabilities of all events is 1 - so the probability of a simple
# event *not* happening is 1 minus that of it happening.
# The probability of two independent events occurring together is the product
# of the probabilities of the events, e.g. that of rolling successive 6's on a (fair)
# die is 1/6 * 1/6 = 1/36.

# The algorithm used in this script makes use of all of the above. The event here is
# two or more people *not* sharing a birthday. Starting with a single person, there
# is a certainty that the event cannot happen, a probability of 1. As more people
# are added, the probability decreases, very slightly at first. Eventually the
# probability will drop below 0.5 - at this point, there is a better-than-evens chance
# of two people sharing a birthday.

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
    print('Only %d people are needed for a better-than-evens chance of 2 sharing a birthday' % people)