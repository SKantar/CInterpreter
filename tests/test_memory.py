import unittest
from interpreter.interpreter.memory import Memory

class TestMemory(unittest.TestCase):

    def test_memory(self):
        memory = Memory()
        memory.declare('a')
        memory['a'] = 1
        memory.declare('b')
        memory['b'] = 2
        memory['a'] = 3
        memory.declare('z')
        memory['z'] = 3
        memory.new_frame('main')
        memory.declare('a')
        memory['a'] = 1
        memory['b'] = 2
        memory['a'] = 3
        memory.new_scope()
        memory.declare('a')
        memory['a'] = 2
        memory.new_frame('test')
        memory.declare('a')
        memory['a'] = 2
        memory.del_frame()
        memory.del_scope()
        memory['s'] = 5
        print(memory['z'])
        print(memory)

