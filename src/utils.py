import itertools


def flatten_array(arr):
    return list(itertools.chain.from_iterable(arr))