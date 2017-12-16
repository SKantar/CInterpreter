from .memory import *
from .number import Number
from ..lexical_analysis.lexer import Lexer
from ..lexical_analysis.token_type import *
from ..syntax_analysis.parser import Parser
from ..syntax_analysis.tree import *
from ..semantic_analysis.analyzer import SemanticAnalyzer
from ..utils.utils import get_functions, MessageColor

class Interpreter(NodeVisitor):

    def __init__(self):
        self.memory = Memory()

    def load_libraries(self, tree):
        for node in filter(lambda o: isinstance(o, IncludeLibrary), tree.children):
            functions = get_functions('interpreter.__builtins__.{}'.format(
                node.library_name
            ))

            for function in functions:
                self.memory[function.__name__] = function

    def load_functions(self, tree):
        for node in filter(lambda o: isinstance(o, FunctionDecl), tree.children):
            self.memory[node.func_name] = node

    def visit_Program(self, node):
        for var in filter(lambda self: not isinstance(self, (FunctionDecl, IncludeLibrary)), node.children):
            self.visit(var)

    def visit_VarDecl(self, node):
        self.memory.declare(node.var_node.value)

    def visit_FunctionDecl(self, node):
        for i, param in enumerate(node.params):
            self.memory[param.var_node.value] = self.memory.stack.current_frame.current_scope._values.pop(i)
        return self.visit(node.body)

    def visit_FunctionBody(self, node):
        for child in node.children:
            if isinstance(child, ReturnStmt):
                return self.visit(child)
            self.visit(child)

    def visit_Expression(self, node):
        expr = None
        for child in node.children:
            expr = self.visit(child)
        return expr

    def visit_FunctionCall(self, node):

        args = [self.visit(arg) for arg in node.args]
        if node.name == 'scanf':
            args.append(self.memory)

        if isinstance(self.memory[node.name], Node):
            self.memory.new_frame(node.name)

            for i, arg in enumerate(args):
                self.memory.declare(i)
                self.memory[i] = arg

            res = self.visit(self.memory[node.name])
            self.memory.del_frame()
            return res
        else:
            return Number(self.memory[node.name].return_type, self.memory[node.name](*args))

    def visit_UnOp(self, node):
        if node.prefix:
            if node.op.type == AND_OP:
                return node.expr.value
            elif node.op.type == INC_OP :
                self.memory[node.expr.value] += Number('int', 1)
                return self.memory[node.expr.value]
            elif node.op.type == DEC_OP:
                self.memory[node.expr.value] -= Number('int', 1)
                return self.memory[node.expr.value]
            elif node.op.type == SUB_OP:
                return Number('int', -1) * self.visit(node.expr)
            elif node.op.type == ADD_OP:
                return self.visit(node.expr)
            elif node.op.type == LOG_NEG:
                res = self.visit(node.expr)
                return res._not()
            else:
                res = self.visit(node.expr)
                return Number(node.op.value, res.value)
        else:
            if node.op.type == INC_OP :
                var = self.memory[node.expr.value]
                self.memory[node.expr.value] += Number('int', 1)
                return var
            elif node.op.type == DEC_OP:
                var = self.memory[node.expr.value]
                self.memory[node.expr.value] -= Number('int', 1)
                return var

        return self.visit(node.expr)

    def visit_CompoundStmt(self, node):
        self.memory.new_scope()

        for child in node.children:
            self.visit(child)

        self.memory.del_scope()

    def visit_ReturnStmt(self, node):
        return self.visit(node.expression)

    def visit_Num(self, node):
        if node.token.type == INTEGER_CONST:
            return Number(ttype="int", value=node.value)
        elif node.token.type == CHAR_CONST:
            return Number(ttype="char", value=node.value)
        else:
            return Number(ttype="float", value=node.value)

    def visit_Var(self, node):
        return self.memory[node.value]

    def visit_Assign(self, node):
        var_name = node.left.value
        if node.op.type == ADD_ASSIGN:
            self.memory[var_name] += self.visit(node.right)
        elif node.op.type == SUB_ASSIGN:
            self.memory[var_name] -= self.visit(node.right)
        elif node.op.type == MUL_ASSIGN:
            self.memory[var_name] *= self.visit(node.right)
        elif node.op.type == DIV_ASSIGN:
            self.memory[var_name] /= self.visit(node.right)
        else:
            self.memory[var_name] = self.visit(node.right)
        return self.memory[var_name]

    def visit_NoOp(self, node):
        pass

    def visit_BinOp(self, node):
        if node.op.type == ADD_OP:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == SUB_OP:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL_OP:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV_OP:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == MOD_OP:
            return self.visit(node.left) % self.visit(node.right)
        elif node.op.type == LT_OP:
            return self.visit(node.left) < self.visit(node.right)
        elif node.op.type == GT_OP:
            return self.visit(node.left) > self.visit(node.right)
        elif node.op.type == LE_OP:
            return self.visit(node.left) <= self.visit(node.right)
        elif node.op.type == GE_OP:
            return self.visit(node.left) >= self.visit(node.right)
        elif node.op.type == EQ_OP:
            return self.visit(node.left) == self.visit(node.right)
        elif node.op.type == NE_OP:
            return self.visit(node.left) != self.visit(node.right)
        elif node.op.type == LOG_AND_OP:
            return self.visit(node.left) and self.visit(node.right)
        elif node.op.type == LOG_OR_OP:
            return self.visit(node.left) or self.visit(node.right)
        elif node.op.type == AND_OP:
            return self.visit(node.left) & self.visit(node.right)
        elif node.op.type == OR_OP:
            return self.visit(node.left) | self.visit(node.right)
        elif node.op.type == XOR_OP:
            return self.visit(node.left) ^ self.visit(node.right)

    def visit_String(self, node):
        return node.value

    def visit_IfStmt(self, node):
        if self.visit(node.condition):
            self.visit(node.tbody)
        else:
            self.visit(node.fbody)

    def visit_WhileStmt(self, node):
        while self.visit(node.condition):
            self.visit(node.body)

    def visit_ForStmt(self, node):
        self.visit(node.setup)
        while self.visit(node.condition):
            self.visit(node.body)
            self.visit(node.increment)

    def interpret(self, tree):
        self.load_libraries(tree)
        self.load_functions(tree)
        self.visit(tree)
        self.memory.new_frame('main')
        node = self.memory['main']
        res = self.visit(node)
        self.memory.del_frame()
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


