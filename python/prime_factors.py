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
        # All integers are divisible by 1 so the factoring is now complete
        if dividend == 1:
            logging.debug('Dividend is now 1 - prime factoring is complete')
            break

        # The number is a prime if there are no factors found and the divisor is past the square root
        if not factors and pow(divisor, 2) > number:
            logging.debug('No factors have been found and the divisor %d is larger than the square root of %d - quitting loop' % (divisor, number))
            break

        # If the divisor is prime and is a factor then capture and retry
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

        # Otherwise try the next integer
        divisor += 1

    return factors


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    factors = prime_factors(args.number)
    if not factors:
        print('No prime factors found - %d is a prime number' % args.number)
    else:
        print(factors)
