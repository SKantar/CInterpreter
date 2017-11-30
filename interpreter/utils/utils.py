from functools import wraps
import pickle
import importlib

def import_module(libname):
    return importlib.import_module(libname)

def get_all_module_func(libname):
    lib = import_module(libname)
    return [func for func in dir(lib) if not func.startswith('__')]

def restorable(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        state = pickle.dumps(self.__dict__)
        result = fn(self, *args, **kwargs)
        self.__dict__ = pickle.loads(state)
        return result
    return wrapper
