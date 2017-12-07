class Scope(object):
    def __init__(self, scope_name, parent_scope):
        self.scope_name = scope_name
        self._values = dict()
        self.parent_scope = parent_scope

    def __setitem__(self, key, value):
        self._values[key] = value

    def __getitem__(self, item):
        return self._values[item]

    def __contains__(self, key):
        return key in self._values



class Frame(object):
    def __init__(self, frame_name):
        self.current_scope = Scope('{}.scope_00'.format(frame_name))

    def new_scope(self):
        current_scope = self.current_scope
        self.current_scope = Scope(
            '{}{}'.format(current_scope[:-2], int(current_scope[-2:])),
            current_scope
        )

    def del_scope(self):
        current_scope = self.current_scope
        self.current_scope = current_scope.parent_scope
        del current_scope

    def __setitem__(self, key, value):
        self.current_scope[key] = value

    def __getitem__(self, item):
        return self.current_scope[item]

    def __contains__(self, key):
        return key in self.current_scope


class Stack(object):
    def __init__(self):
        self.frames = list()
        self.current_frame = None

    def __bool__(self):
        return bool(self.frames)

    def push(self, frame_name):
        frame = Frame(frame_name)
        self.frames.append(frame)
        self.current_frame = frame

    def pop(self):
        self.frames.pop(-1)
        self.current_frame = len(self.frames) and self.frames[-1] or None


class Memory(object):
    def __init__(self):
        self.global_scope = Frame('GLOBAL_MEMORY')
        self.stack = Stack()

    def __setitem__(self, key, value):
        if self.stack.current_frame:
            self.stack.current_frame[key] = value
        else:
            self.global_scope[key] = value

    def __getitem__(self, item):
        if item in self.stack.current_frame:
            return self.stack.current_frame[item]
        return self.global_scope[item]

    def create_frame(self, frame_name):
        self.stack.push(frame_name)

    def remove_frame(self):
        self.stack.pop()


