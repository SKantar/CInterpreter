from functools import wraps


def multi(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if not isinstance(res, list):
            return [res]
        return res
    return wrapper