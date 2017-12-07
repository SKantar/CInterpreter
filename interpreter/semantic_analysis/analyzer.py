from ..syntax_analysis.tree import NodeVisitor, Type
from ..syntax_analysis.parser import INTEGER_CONST, REAL_CONST
from .table import *
from ..utils.utils import get_all_module_func, get_name
from .types import CType
import warnings


class SemanticError(Exception):
    pass

class TypeError(UserWarning):
    pass

class SemanticAnalyzer(NodeVisitor):

    def __init__(self):
        self.current_scope = None

    def error(self, message):
        raise SemanticError(message)

    def warning(self, message):
        warnings.warn(message)

    def visit_Program(self, node, *args, **kwargs):
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope, # None
        )
        global_scope._init_builtins()
        self.current_scope = global_scope

        for child in node.children:
            self.visit(child)


        # print(self.current_scope)
        self.current_scope = self.current_scope.enclosing_scope

    def visit_VarDecl(self, node, *args, **kwargs):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        # Signal an error if the table alrady has a symbol
        # with the same name
        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.insert(var_symbol)

    def visit_IncludeLibrary(self, node, *args, **kwargs):
        functions = get_all_module_func('interpreter.__builtins__.{}'.format(
            node.library_name
        ))

        for func in functions:
            type_symbol = self.current_scope.lookup(func.return_type)

            func_symbol = FunctionSymbol(func.__name__, type=type_symbol)

            if func.arg_types == None:
                func_symbol.params = None
            else:
                for i, param_type in enumerate(func.arg_types):
                    type_symbol = self.current_scope.lookup(param_type)
                    var_symbol = VarSymbol('param{:02d}'.format(i + 1), type_symbol)
                    func_symbol.params.append(var_symbol)

            self.current_scope.insert(func_symbol)

    def visit_FunctionDecl(self, node, *args, **kwargs):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        func_name = node.func_name
        if self.current_scope.lookup(func_name):
            self.error(
                "Error: Duplicate identifier '%s' found" % func_name
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

        kwargs['function'] = True
        self.visit(node.body, *args, **kwargs)

        self.current_scope = self.current_scope.enclosing_scope

    def visit_Param(self, node, *args, **kwargs):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, current_scope_only=True):
            self.error(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.insert(var_symbol)
        return var_symbol

    def visit_CompoundStmt(self, node, *args, **kwargs):
        if 'function' not in kwargs:
            procedure_scope = ScopedSymbolTable(
                scope_name=get_name(self.current_scope.scope_name),
                scope_level=self.current_scope.scope_level + 1,
                enclosing_scope=self.current_scope
            )
            self.current_scope = procedure_scope

        for child in node.children:
            self.visit(child, *args, **kwargs)

    def visit_BinOp(self, node, *args, **kwargs):
        return self.visit(node.left, *args, **kwargs) + self.visit(node.right, *args, **kwargs)

    def visit_UnOp(self, node, *args, **kwargs):
        if isinstance(node.op, Type):
            return CType(node.op.value)
        return self.visit(node.expr, *args, **kwargs)

    def visit_TerOp(self, node, *args, **kwargs):
        self.visit(node.condition, *args, **kwargs)
        texpr = self.visit(node.texpression, *args, **kwargs)
        fexpr = self.visit(node.fexpression, *args, **kwargs)
        if texpr != fexpr:
            self.warning("Incompatibile types at ternary operator texpr:<{}> fexpr:<{}>".format(
                texpr,
                fexpr
            ))
        return texpr

    def visit_Assign(self, node, *args, **kwargs):
        right = self.visit(node.right, *args, **kwargs)
        left = self.visit(node.left, *args, **kwargs)
        if left != right:
            self.warning("Incompatibile types <{}> {} <{}>".format(
                left,
                node.op.value,
                right
            ))
        return right

    def visit_Var(self, node, *args, **kwargs):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            self.error(
                "Symbol(identifier) not found '%s'" % var_name
            )
        return CType(var_symbol.type.name)

    def visit_Type(self, node, *args, **kwargs):
        pass

    def visit_IfStmt(self, node, *args, **kwargs):
        self.visit(node.condition, *args, **kwargs)
        self.visit(node.tbody, *args, **kwargs)
        self.visit(node.fbody, *args, **kwargs)

    def visit_WhileStmt(self, node, *args, **kwargs):
        self.visit(node.condition, *args, **kwargs)
        self.visit(node.body, *args, **kwargs)

    def visit_DoWhileStmt(self, node, *args, **kwargs):
        self.visit(node.condition, *args, **kwargs)
        self.visit(node.body, *args, **kwargs)

    def visit_ReturnStmt(self, node, *args, **kwargs):
        return self.visit(node.expression, *args, **kwargs)

    def visit_Num(self, node, *args, **kwargs):
        if node.token.type == INTEGER_CONST:
            return CType("int")
        else:
            return CType("Float")

    def visit_String(self, node, *args, **kwargs):
        pass

    def visit_NoOp(self, node, *args, **kwargs):
        pass

    def visit_FunctionCall(self, node, *args, **kwargs):
        func_name = node.name
        func_symbol = self.current_scope.lookup(func_name)
        if func_symbol is None:
            self.error(
                "Function '%s' not found" % func_name
            )

        if not isinstance(func_symbol, FunctionSymbol):
            self.error(
                "Identifier '%s' cannot be used as a function" % func_name
            )


        if func_symbol.params != None:
            if len(node.args) != len(func_symbol.params):
                self.error(
                    "Function {} takes {} positional arguments but {} were given".format(
                        func_name,
                        len(node.params),
                        len(func_symbol.params)
                    )
                )

            expected = []
            found = []
            for i, arg in enumerate(node.args):
                arg_type = self.visit(arg, *args, **kwargs)
                param_type = CType(func_symbol.params[i].type.name)
                expected.append(param_type)
                found.append(arg_type)
            if expected != found:
                self.warning("Incompatibile argument types for function <{}{}> but found <{}{}>".format(
                    func_name,
                    str(expected).replace('[', '(').replace(']', ')'),
                    func_name,
                    str(found).replace('[', '(').replace(']', ')')
                ))

        return CType(func_symbol.type.name)

    def visit_Expression(self, node, *args, **kwargs):
        expr = None
        for child in node.children:
            expr = self.visit(child, *args, **kwargs)
        return expr

    @staticmethod
    def analyze(tree):
        semantic_analyzer = SemanticAnalyzer()
        semantic_analyzer.visit(tree)