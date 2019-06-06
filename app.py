import time

import redis

from waitress import serve
from flask import Flask
from sympy.ntheory import isprime

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def calculate_prime(n) -> bool:
    if cache.exists(n):
        return True
        
    else:
        # Miller–Rabin primality test proved for all n < 2^64
        if isprime(n):
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
    return ' '.join([str(int(k)) for k in cache.keys()])

@app.route('/clearKeys')
def clearKeys():
    cache.flushdb()
    return "Keys cleared"

serve(app, host='0.0.0.0', port=5000)
