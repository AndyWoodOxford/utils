#!/usr/bin/env python3

N = 5

def args():
    pass

def factorial(n):
    if n < 0:
        raise ValueError('Invalid value %d - n must be positive' % n)

    result = 1
    for i in range(1, n + 1):
        result *= i

    return result

if __name__ == '__main__':
    answer = factorial(N)
    print('Result = %d' % answer)