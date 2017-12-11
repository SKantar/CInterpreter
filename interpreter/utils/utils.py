from functools import wraps
import pickle
import importlib

def import_module(libname):
    return importlib.import_module(libname)

def get_functions(module):
    lib = import_module(module)

    for func_name in dir(lib):
        func = getattr(lib, func_name)
        if callable(func) and not func_name.startswith('__') and func.__module__.endswith(module):
            yield func

def restorable(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        state = pickle.dumps(self.__dict__)
        result = fn(self, *args, **kwargs)
        self.__dict__ = pickle.loads(state)
        return result
    return wrapper


def definition(return_type=None, arg_types=[]):
    def wrapper_decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs)
        wrapper.return_type = return_type
        wrapper.arg_types = arg_types
        return wrapper
    return wrapper_decorator


def get_name(name):
    if name[-2:].isdigit():
        return '{}{:02d}'.format(
            name[:-2],
            int(name[-2:]) + 1
        )
    else:
        return '{}{:02d}'.format(
            name,
            1
        )


class MessageColor:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'






