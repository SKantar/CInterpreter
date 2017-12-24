from ..syntax_analysis.tree import NodeVisitor, Type
from ..syntax_analysis.parser import INTEGER_CONST, CHAR_CONST, AND_OP, OR_OP, XOR_OP
from .table import *
from ..utils.utils import get_functions, get_name, MessageColor

class SemanticError(Exception):
    pass

class TypeError(UserWarning):
    pass

class SemanticAnalyzer(NodeVisitor):

    class CType(object):
        types = dict(char=int, int=int, float=float, double=float)
        order = ('char', 'int', 'float', 'double')

        def __init__(self, ttype):
            self.type = ttype

        def _calc_type(self, other):
            left_order = SemanticAnalyzer.CType.order.index(self.type)
            right_order = SemanticAnalyzer.CType.order.index(other.type)
            return SemanticAnalyzer.CType(SemanticAnalyzer.CType.order[max(left_order, right_order)])

        def __add__(self, other):
            return self._calc_type(other)

        def __eq__(self, other):
            return SemanticAnalyzer.CType.types[self.type] == SemanticAnalyzer.CType.types[other.type]

        def __repr__(self):
            return '{}'.format(self.type)

        def __str__(self):
            return self.__repr__()

    def __init__(self):
        self.current_scope = None

    def error(self, message):
        raise SemanticError(message)

    def warning(self, message):
        print(MessageColor.WARNING + message + MessageColor.ENDC)

    def visit_Program(self, node):
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope,
        )
        global_scope._init_builtins()
        self.current_scope = global_scope

        for child in node.children:
            self.visit(child)

        if not self.current_scope.lookup('main'):
            self.error(
                "Error: Undeclared mandatory function main"
            )

        self.current_scope = self.current_scope.enclosing_scope

    def visit_VarDecl(self, node):
        """ type_node var_node """

        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                "Error: Duplicate identifier '{}' found at line {}".format(
                    var_name,
                    node.line
                )
            )

        self.current_scope.insert(var_symbol)

    def visit_IncludeLibrary(self, node):
        """ #include <library_name.h> """

        functions = get_functions('interpreter.__builtins__.{}'.format(
            node.library_name
        ))

        for func in functions:
            type_symbol = self.current_scope.lookup(func.return_type)

            func_name = func.__name__
            if self.current_scope.lookup(func_name):
                continue

            func_symbol = FunctionSymbol(func_name, type=type_symbol)

            if func.arg_types == None:
                func_symbol.params = None
            else:
                for i, param_type in enumerate(func.arg_types):
                    type_symbol = self.current_scope.lookup(param_type)
                    var_symbol = VarSymbol('param{:02d}'.format(i + 1), type_symbol)
                    func_symbol.params.append(var_symbol)

            self.current_scope.insert(func_symbol)

    def visit_FunctionDecl(self, node):
        """ type_node  func_name ( params ) body """

        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        func_name = node.func_name
        if self.current_scope.lookup(func_name):
            self.error(
                "Error: Duplicate identifier '{}' found at line {}".format(func_name, node.line)
            )
        func_symbol = FunctionSymbol(func_name, type=type_symbol)
        self.current_scope.insert(func_symbol)

        procedure_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        for param in node.params:
            func_symbol.params.append(self.visit(param))

        self.visit(node.body)

        self.current_scope = self.current_scope.enclosing_scope

    def visit_FunctionBody(self, node):
        """ { children } """
        for child in node.children:
            self.visit(child)

    def visit_Param(self, node):
        """ type_node var_node """

        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                "Error: Duplicate identifier '{}' found at line {}".format(
                    var_name,
                    node.line
                )
            )

        self.current_scope.insert(var_symbol)
        return var_symbol

    def visit_CompoundStmt(self, node):
        """ { children } """

        procedure_scope = ScopedSymbolTable(
            scope_name=get_name(self.current_scope.scope_name),
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        for child in node.children:
            self.visit(child)

        self.current_scope = self.current_scope.enclosing_scope

    def visit_BinOp(self, node):
        """ left op right """
        ltype = self.visit(node.left)
        rtype = self.visit(node.right)
        if node.op.type == AND_OP or node.op.type == OR_OP or node.op.type == XOR_OP:
            if ltype.type != "int" or rtype.type != "int":
                self.error("Unsupported types at bitwise operator ltype:<{}> rtype:<{}> at line {}".format(
                    ltype.type,
                    rtype.type,
                    node.line
                ))
        return ltype + rtype 

    def visit_UnOp(self, node):
        """ op expr """
        if isinstance(node.op, Type):
            self.visit(node.expr)
            return SemanticAnalyzer.CType(node.op.value)
        return self.visit(node.expr)

    def visit_TerOp(self, node):
        """ condition ? texpression : fexpression """
        self.visit(node.condition)
        texpr = self.visit(node.texpression)
        fexpr = self.visit(node.fexpression)
        if texpr != fexpr:
            self.warning("Incompatibile types at ternary operator texpr:<{}> fexpr:<{}> at line {}".format(
                texpr,
                fexpr,
                node.line
            ))
        return texpr

    def visit_Assign(self, node):
        """ right = left """
        right = self.visit(node.right)
        left = self.visit(node.left)
        if left != right:
            self.warning("Incompatible types when assigning to type <{}> from type <{}> at line {}".format(
                left,
                right,
                node.line
            ))
        return right

    def visit_Var(self, node):
        """ value """
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(
                "Symbol(identifier) not found '{}' at line {}".format(
                    var_name,
                    node.line
                )
            )
        return SemanticAnalyzer.CType(var_symbol.type.name)

    def visit_Type(self, node):
        pass

    def visit_IfStmt(self, node):
        """ if (condition) tbody else fbody """
        self.visit(node.condition)
        self.visit(node.tbody)
        self.visit(node.fbody)

    def visit_ForStmt(self, node):
        """ for(setup condition increment) body"""
        self.visit(node.setup)
        self.visit(node.condition)
        self.visit(node.increment)
        self.visit(node.body)

    def visit_WhileStmt(self, node):
        """ while(condition) body """
        self.visit(node.condition)
        self.visit(node.body)

    def visit_DoWhileStmt(self, node):
        """ do body while (condition) """
        self.visit(node.condition)
        self.visit(node.body)

    def visit_ReturnStmt(self, node):
        """ return expression """
        return self.visit(node.expression)

    def visit_Num(self, node):
        """ value """
        if node.token.type == INTEGER_CONST:
            return SemanticAnalyzer.CType("int")
        elif node.token.type == CHAR_CONST:
            return SemanticAnalyzer.CType("char")
        else:
            return SemanticAnalyzer.CType("float")

    def visit_String(self, node):
        pass

    def visit_NoOp(self, node):
        pass

    def visit_FunctionCall(self, node):
        func_name = node.name
        func_symbol = self.current_scope.lookup(func_name)
        if func_symbol is None:
            self.error(
                "Function '{}' not found at line {}".format(
                    func_name,
                    node.line
            ))

        if not isinstance(func_symbol, FunctionSymbol):
            self.error(
                "Identifier '{}' cannot be used as a function at line".format(
                    func_name,
                    node.line
                )
            )

        if func_symbol.params == None:
            for i, arg in enumerate(node.args):
                self.visit(arg)
            return SemanticAnalyzer.CType(func_symbol.type.name)

        if len(node.args) != len(func_symbol.params):
            self.error(
                "Function {} takes {} positional arguments but {} were given at line {}".format(
                    func_name,
                    len(node.args),
                    len(func_symbol.params),
                    node.line
                )
            )

        expected = []
        found = []

        for i, arg in enumerate(node.args):
            arg_type = self.visit(arg)
            param_type = SemanticAnalyzer.CType(func_symbol.params[i].type.name)
            expected.append(param_type)
            found.append(arg_type)

        if expected != found:
            self.warning("Incompatibile argument types for function <{}{}> but found <{}{}> at line {}".format(
                func_name,
                str(expected).replace('[', '(').replace(']', ')'),
                func_name,
                str(found).replace('[', '(').replace(']', ')'),
                node.line
            ))

        return SemanticAnalyzer.CType(func_symbol.type.name)

    def visit_Expression(self, node):
        expr = None
        for child in node.children:
            expr = self.visit(child)
        return expr

    @staticmethod
    def analyze(tree):
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)