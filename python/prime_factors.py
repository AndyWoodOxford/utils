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


# 1. need "retries" for each divisor e.g. 24 => 2,2,2,3
# 2. factor itself must be prime => separate function, abort as soon as a smaller factor is found?

def is_prime(number):
    factor = 2
    while factor < number:
        if number % factor == 0:
            return False
        factor += 1
    return True


def prime_factors(number):
    logging.debug('Calculating prime factors for %d' % number)
    factors = ()
    dividend = number
    divisor = 2
    while True:
        logging.debug('Trying divisor %d' % divisor)
        if is_prime(divisor):
            logging.debug('  Divisor is a prime')
            if dividend % divisor == 0:
                # Divisor is a prime factor - capture and retry this value
                logging.debug('  Divisor is a prime factor')
                factors += (divisor,)
                dividend = dividend // divisor
                logging.debug('  Dividend is now %d' % dividend)
                continue
            else:
                logging.debug('  Divisor is not a prime factor')
        else:
            logging.debug('Divisor is not a prime')

        # All integers are divisible by 1 so the work is complete
        if dividend == 1:
            logging.debug('Dividend is now 1 - prime factoring is complete')
            break

        # Current divisor has now been drained - increment
        logging.debug('HERE')
        divisor += 1

    return factors


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    answer = prime_factors(args.number)
    print(answer)
