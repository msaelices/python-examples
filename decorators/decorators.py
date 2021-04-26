# %%

import time
from functools import wraps

_cache = {}


def cached(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key in _cache:
            return _cache[cache_key]
        result = func(*args, **kwargs)
        _cache[cache_key] = result
        return result

    return wrapper


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        result = func(*args, **kwargs)
        t2 = time.time()
        print(f'{func.__name__} with args={args} and kwargs={kwargs} took {t2 - t1} seconds')
        return result
    return wrapper


# %%

@timer
@cached
def fib(n):
    """Return the Fibonacci function result of an integer"""
    return fib(n - 1) + fib(n - 2) if n > 1 else n


print(fib(6))

# %%
