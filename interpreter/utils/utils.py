from functools import wraps
import pickle

def multi(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        res = fn(*args, **kwargs)
        if not isinstance(res, list):
            return [res]
        return res
    return wrapper

def restorable(fn):
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        state = pickle.dumps(self.__dict__)
        result = fn(self, *args, **kwargs)
        self.__dict__ = pickle.loads(state)
        return result
    return wrapper

if __name__ == '__main__':

    class B(object):
        def __init__(self):
            self.b = 3


    class A(object):
        def __init__(self):
            self.a = 1
            self.b = B()

        @restorable
        def check(self):
            self.a = 2
            self.b.b = 4


    a = A()
    print(a.a, a.b.b)
    a.check()
    print(a.a, a.b.b)
