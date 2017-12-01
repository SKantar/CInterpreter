from .memory import *
from ..lexical_analysis.lexer import Lexer
from ..lexical_analysis.token_type import *
from ..syntax_analysis.parser import Parser
from ..syntax_analysis.tree import *
from ..semantic_analysis.analyzer import SemanticAnalyzer
from ..utils.utils import import_module, MessageColor

class Interpreter(NodeVisitor):

    def __init__(self):
        self.memory = Memory()

    def load_functions(self, tree):
        for node in filter(lambda o: isinstance(o, FunctionDecl), tree.children):
            self.memory[node.func_name] = node

    def load_libraries(self, tree):
        for node in filter(lambda o: isinstance(o, IncludeLibrary), tree.children):
            lib = import_module('interpreter.__builtins__.{}'.format(
                node.library_name
            ))

            for attr in dir(lib):
                if not attr.startswith('__'):
                    self.memory[attr] = getattr(lib, attr)

    def visit_Program(self, node):
        for var in filter(lambda self: not isinstance(self, (FunctionDecl, IncludeLibrary)), node.children):
            self.visit(var)

    def visit_VarDecl(self, node):
        self.memory[node.var_node.value] = None

    def visit_Assign(self, node):
        var_name = node.left.value
        var_value = self.visit(node.right)
        self.memory[var_name] = var_value

    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == LT:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GT:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LE:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GE:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == EQ:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NE:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == AND:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == OR:
            return self.visit(node.left) or self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_UnaryOp(self, node):
        op = node.op.type
        if op == PLUS:
            return +self.visit(node.expr)
        elif op == MINUS:
            return -self.visit(node.expr)
        elif op == AMPERSAND:
            return node.expr.value
        elif op == NOT:
            return int(not bool(self.visit(node.expr)))

    def visit_FunctionCall(self, node):

        params = [self.visit(param) for param in node.params]

        if isinstance(self.memory[node.func_name], Node):
            self.memory.create_frame(node.func_name)

            for i, param in enumerate(params):
                self.memory[i] = param
            res = self.visit(self.memory[node.func_name])
            self.memory.remove_frame()
            return res
        else:
            return self.memory[node.func_name](*params, memory=self.memory)

    def visit_FunctionDecl(self, node):
        for i, param in enumerate(node.params):
            self.memory[param.var_node.value] = self.memory.stack.current_frame._values.pop(i)
        return self.visit(node.body)

    def visit_Body(self, node):
        for child in node.children:
            if isinstance(child, ReturnStmt):
                return self.visit(child)
            self.visit(child)

    def visit_ReturnStmt(self, node):
        return self.visit(node.expr)

    def visit_Var(self, node):
        return self.memory[node.value]

    def visit_String(self, node):
        return node.value

    def visit_IfStmt(self, node):
        if self.visit(node.condition_stmt):
            self.visit(node.if_body)
        else:
            self.visit(node.else_body)

    def visit_WhileStmt(self, node):
        while self.visit(node.condition_stmt):
            self.visit(node.body)

    def interpret(self, tree):
        self.load_libraries(tree)
        self.load_functions(tree)
        self.visit(tree)
        self.memory.create_frame('main')
        node = self.memory['main']
        res = self.visit(node)
        self.memory.remove_frame()
        return res

    @staticmethod
    def run(program):
        try:
            lexer = Lexer(program)
            parser = Parser(lexer)
            tree = parser.parse()
            SemanticAnalyzer.analyze(tree)
            status = Interpreter().interpret(tree)
        except Exception as message:
            print("{}[{}] {} {}".format(
                MessageColor.FAIL,
                type(message).__name__,
                message,
                MessageColor.ENDC
            ))
            status = -1
        print()
        print(MessageColor.OKBLUE + "Process terminated with status {}".format(status) + MessageColor.ENDC)


