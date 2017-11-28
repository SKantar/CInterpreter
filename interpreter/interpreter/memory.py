class Frame(object):
    def __init__(self, frame_name):
        # print("Create frame {}".format(frame_name))
        self.frame_name = frame_name
        self._values = dict()

    def __setitem__(self, key, value):
        self._values[key] = value

    def __getitem__(self, item):
        return self._values[item]

    def __contains__(self, key):
        return key in self._values


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
        self.global_frame = Frame('GLOBAL_MEMORY')
        self.stack = Stack()

    def __setitem__(self, key, value):
        if self.stack.current_frame:
            self.stack.current_frame[key] = value
        else:
            self.global_frame[key] = value

    def __getitem__(self, item):
        if item in self.stack.current_frame:
            return self.stack.current_frame[item]
        return self.global_frame[item]

    def create_frame(self, frame_name):
        self.stack.push(frame_name)

    def remove_frame(self):
        self.stack.pop()


