from ..syntax_analysis.tree import NodeVisitor
from .table import *

class SemanticAnalyzer(NodeVisitor):

    def __init__(self):
        self.current_scope = None

    def visit_Program(self, node):
        # print('ENTER scope: global')
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=1,
            enclosing_scope=self.current_scope, # None
        )
        global_scope._init_builtins()
        self.current_scope = global_scope

        for child in node.children:
            self.visit(child)

        # print(global_scope)

        self.current_scope = self.current_scope.enclosing_scope
        # print('LEAVE scope: global')

    def visit_VarDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        # Signal an error if the table alrady has a symbol
        # with the same name
        if self.current_scope.lookup(var_name, current_scope_only=True):
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.insert(var_symbol)

    def visit_FunctionDecl(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        func_name = node.func_name
        if self.current_scope.lookup(func_name):
            raise Exception(
                "Error: Duplicate identifier '%s' found" % func_name
            )
        func_symbol = FunctionSymbol(func_name, type=type_symbol)
        self.current_scope.insert(func_symbol)

        # print('ENTER scope: %s' % func_name)
        # Scope for parameters and local variables
        procedure_scope = ScopedSymbolTable(
            scope_name=func_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope
        )
        self.current_scope = procedure_scope

        # Insert parameters into the procedure scope
        for param in node.params:
            func_symbol.params.append(self.visit(param))
            # param_type = self.current_scope.lookup(param.type_node.value)
            # param_name = param.var_node.value
            # var_symbol = VarSymbol(param_name, param_type)
            # self.current_scope.insert(var_symbol)
            # func_symbol.params.append(var_symbol)

        self.visit(node.body)

        # print(procedure_scope)

        self.current_scope = self.current_scope.enclosing_scope
        # print('LEAVE scope: %s' % func_name)

    def visit_Param(self, node):
        type_name = node.type_node.value
        type_symbol = self.current_scope.lookup(type_name)

        var_name = node.var_node.value
        var_symbol = VarSymbol(var_name, type_symbol)

        if self.current_scope.lookup(var_name, current_scope_only=True):
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        self.current_scope.insert(var_symbol)
        return var_symbol

    def visit_Body(self, node):
        for child in node.children:
            self.visit(child)

    def visit_BinOp(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node):
        self.visit(node.expr)

    def visit_Assign(self, node):
        self.visit(node.right)
        self.visit(node.left)

    def visit_Var(self, node):
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_Type(self, node):
        pass

    def visit_Block(self, node):
        for child in node.children:
            self.visit(child)

    def visit_IfStmt(self, node):
        self.visit(node.condition_stmt)
        self.visit(node.if_body)
        self.visit(node.else_body)

    def visit_ReturnStmt(self, node):
        self.visit(node.expr)

    def visit_Num(self, node):
        pass

    def visit_NoOp(self, node):
        pass

    def visit_FunctionCall(self, node):
        func_name = node.func_name
        func_symbol = self.current_scope.lookup(func_name)
        if func_symbol is None:
            raise Exception(
                "Function '%s' not found" % func_name
            )

        if not isinstance(func_symbol, FunctionSymbol):
            raise Exception(
                "Identifier '%s' cannot be used as a function" % func_name
            )

        if len(node.params) != len(func_symbol.params):
            raise Exception(
                "Function {} takes {} positional arguments but {} were given".format(
                    func_name,
                    len(node.params),
                    len(func_symbol.params)
                )
            )


    @staticmethod
    def analyze(tree):
        semantic_analyzer = SemanticAnalyzer()
        try:
            semantic_analyzer.visit(tree)
        except Exception as e:
            raise e