import time

import redis
from flask import Flask

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

# Miller–Rabin primality test proved for all n in [0, 118670087467)
def calculate_prime(n) -> bool:

    if cache.exists(n):
        return True
        
    else:
        def _try_composite(a, d, n, s):
            if pow(a, d, n) == 1:
                return False
            for i in range(s):
                if pow(a, 2**i * d, n) == n-1:
                    return False
            return True # n is definitely composite

        if any((n % p) == 0 for p in [2, 3]) or n in (0, 1):
            return False
        d, s = n - 1, 0
        while not d % 2:
            d, s = d >> 1, s + 1
        isPrime = False
        if n < 1373653: 
            isPrime = not any(_try_composite(a, d, n, s) for a in (2, 3))
        elif n < 25326001: 
            isPrime = not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
        elif n < 118670087467: 
            if n == 3215031751: 
                isPrime = False
            isPrime = not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
        else:
            raise "Number too big for primality check"
        if isPrime:
            cache.set(n, "")
            return True
        return False


@app.route('/isPrime/<int:number>')
def isPrime(number):
    if calculate_prime(number):
        return "{} is prime".format(number)
    else:
        return "{} is not prime".format(number)

@app.route('/primesStored')
def primesStored():
    return '\n'.join([str(int(k)) for k in cache.keys()])
