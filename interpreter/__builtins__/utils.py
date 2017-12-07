from functools import wraps


def definition(return_type=None, arg_types=[]):
    def wrapper_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.return_type = return_type
        wrapper.arg_types = arg_types
        return wrapper
    return wrapper_decorator



