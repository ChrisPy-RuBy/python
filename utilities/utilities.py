import pprint as pp
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
