class Node(object):
    pass


class Program(Node):
    def __init__(self, declarations):
        self.children = declarations


class VarDecl(Node):
    def __init__(self, var_node, type_node):
        self.var_node = var_node
        self.type_node = type_node


class FunctionDecl(Node):
    def __init__(self, type_node, func_name, params, block_node):
        self.type_node = type_node
        self.func_name = func_name
        self.params = params            # a list of Param nodes
        self.block_node = block_node


class Param(Node):
    def __init__(self, type_node, var_node):
        self.var_node = var_node
        self.type_node = type_node


class Type(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Var(Node):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Block(Node):
    def __init__(self, statements):
        self.children = statements


class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(Node):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class UnaryOp(Node):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr


class NoOp(Node):
    pass


class IfStmt(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition_stmt = condition
        self.if_block = if_block
        self.else_block = else_block