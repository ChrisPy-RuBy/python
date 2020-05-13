import pprint as pp
from collections import defaultdict
from functools import wraps
from inspect import getcallargs


def dump_args_and_return(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        input_args = getcallargs(func, *args, **kwargs)
        results = func(*args, **kwargs)
        print("input_args: {}".format(pp.pformat(input_args)))
        print("results: {}".format(pp.pformat(results)))
        return results

    return wrapper


from functools import partial, wraps


def print_result(func=None, *, prefix=""):
    """Useful decorator that prints the results of the 
    function with an optional prefix"""
    if func is None:
        return partial(print_result, prefix=prefix)

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(f"{prefix}{result}")
        return result

    return wrapper


def transpose_table(data):

    """Turn data like this
    data = [{'a': 10, 'b': 14, 'c': 145}, {'a': 654, 'b': 99, 'd': 13}, {'b':12, 'd': 14}]

    into this.
    {'_id': 10, 'a': 1, 'd': 0, 'b': 0, 'c': 0}
    {'_id': 14, 'a': 0, 'd': 1, 'b': 1, 'c': 0}
    {'_id': 145, 'a': 0, 'd': 0, 'b': 0, 'c': 1}
    {'_id': 654, 'a': 1, 'd': 0, 'b': 0, 'c': 0}
    {'_id': 99, 'a': 0, 'd': 0, 'b': 1, 'c': 0}
    {'_id': 13, 'a': 0, 'd': 1, 'b': 0, 'c': 0}
    {'_id': 12, 'a': 0, 'd': 0, 'b': 1, 'c': 0}
    where """

    groupbyvalue = defaultdict(list)
    columns = set()
    results = []
    for row in data:
        for k, v in row.items():
            groupbyvalue[v].append(k)
            columns.add(k)
    for _id, dates in groupbyvalue.items():
        row = {"_id": _id}
        for c in columns:
            if c in dates:
                row[c] = 1
            else:
                row[c] = 0
        results.append(row)
    return results


import time
import math


def retry(func, exception):
    """Exponential retry wrapper for func that raises exception"""
    attempt = 1
    while True:
        try:
            func()
            break
        except exception:
            if attempt > 5:
                break
            timetowait = math.e ** (attempt)
            print("Attempt {}, waiting {} seconds...".format(attempt, timetowait))
            time.sleep(timetowait)
            attempt += 1
        except Exception:
            raise "Something else happened"


def retry_dec(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        attempt = 1
        while True:
            try:
                func(*args, **kwargs)
                break
            except ValueError:
                if attempt > 5:
                    break
                timetowait = math.e ** (attempt)
                print("Attempt {}, waiting {} seconds...".format(attempt, timetowait))
                time.sleep(timetowait)
                attempt += 1
            except Exception:
                raise "Something else happened"

    return wrapper


def retry_dec_with_exception(exception):
    """Decorator that applies a decay curve to retry attempts
    for a specific exception
    """

    def inner_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 1
            while True:
                try:
                    func(*args, **kwargs)
                    break
                except exception:
                    if attempt > 5:
                        break
                    timetowait = math.e ** (attempt)
                    print(
                        "Attempt {}, waiting {} seconds...".format(attempt, timetowait)
                    )
                    time.sleep(timetowait)
                    attempt += 1
                except Exception:
                    raise "Something else happened"

        return wrapper

    return inner_function
