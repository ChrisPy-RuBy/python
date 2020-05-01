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
        row = {'_id': _id}
        for c in columns:
            if c in dates:
                row[c] = 1
            else:
                row[c] = 0
        results.append(row)
    return results

