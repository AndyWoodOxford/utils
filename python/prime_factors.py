#!/usr/bin/env python3

"""
Outputs the prime factors of a positive integer.
"""

import argparse
import colorama
import logging

from colorama import Fore, Style



def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('number', type=int)
    parser.add_argument('-q', '--quiet', help='Quiet mode', action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose mode', action='store_true')
    return parser.parse_args()


def configure_logging(local_args):
    log_level = logging.INFO
    if local_args.quiet:
        log_level = logging.WARNING
    elif local_args.verbose:
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
    factors_set = ()
    dividend = number
    divisor = 2
    while True:
        # All integers are divisible by 1 so the factoring is now complete
        if dividend == 1:
            logging.debug('Dividend is now 1 - prime factoring is complete')
            break

        # The number is a prime if there are no factors found and the divisor is past the square root
        if not factors_set and pow(divisor, 2) > number:
            logging.debug('No factors have been found and the divisor %d is larger than the square root of %d - quitting loop' % (divisor, number))
            break

        # If the divisor is prime and is a factor then capture and retry
        logging.debug('Trying divisor %d' % divisor)
        if is_prime(divisor):
            logging.debug('  Divisor is a prime')
            if dividend % divisor == 0:
                # Divisor is a prime factor - capture and retry this value
                logging.debug('  Divisor is a prime factor')
                factors_set += (divisor,)
                dividend = dividend // divisor
                logging.debug('  Dividend is now %d' % dividend)
                continue

        # Otherwise try the next integer
        divisor += 1

    return factors_set


def output_string(factors):
    index_list = (range(len(factors)))
    factors_indexed = {index: factor for index, factor in zip(index_list, factors)}
    count_distinct = len(set(factors_indexed.values()))

    colorama.init(autoreset=True)

    index = 0
    output = ''
    while index < len(factors):
        prime_factor = factors[index]
        # Unique prime factor - capture and increment to the following one
        if factors.count(prime_factor) == 1:
            output += '%s%d%s' % (Fore.GREEN, prime_factor, Style.RESET_ALL)
            if index < len(factors) - 1:
                output += ' * '
            index += 1
        # Repeated prime factor - construct exponent and shift the index by the count
        else:
            prime_factor_count = factors.count(prime_factor)
            output += '%s%d%s' % (Fore.GREEN,  prime_factor, Style.RESET_ALL)
            output += '%s^%s' % (Style.BRIGHT, Style.RESET_ALL)
            output += '%s%d%s' % (Fore.CYAN,  prime_factor_count, Style.RESET_ALL)
            if index + prime_factor_count < len(factors):
                output += ' * '
            index += prime_factor_count

    return output


if __name__ == '__main__':
    args = parse_args()
    configure_logging(args)

    prime_factors = prime_factors(args.number)
    if not prime_factors:
        print('No factors found: %d is a prime number' % args.number)
    else:
        print('The prime factors of %d are: %s' % (args.number, output_string(prime_factors)))
