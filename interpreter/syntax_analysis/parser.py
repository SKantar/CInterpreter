""" SCI - Simple C Interpreter """

###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################
from ..lexical_analysis.token_type import *
from .tree import *
from ..utils.utils import restorable

class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self, expected=None, obtained=None):
        if not expected and not obtained:
            raise Exception('Invalid syntax')
        else:
            raise Exception('Expected token <{}> but found <{}> at line {}.'.format(
                expected, obtained, self.lexer.line
            ))

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(token_type, self.current_token.type)

    def program(self):
        """
        program                     : declarations
        """
        root = Program(self.declarations())
        return root

    def declarations(self):
        """
        declarations                : (function_declaration | var_declaration_list)*
        """
        declarations = []

        while self.current_token.type == TYPE:
            if self.check_function(declaration=True):
                declarations.append(self.function_declaration())
            else:
                declarations.extend(self.var_declaration_list())
        return declarations

    def function_declaration(self):
        """
        function_declaration        : type_spec ID LPAREN parameters RPAREN function_body
        """
        type_node = self.type_spec()
        func_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        params = self.parameters()
        self.eat(RPAREN)
        return FunctionDecl(
            type_node=type_node,
            func_name=func_name,
            params=params,
            body=self.function_body()
        )

    def function_body(self):
        """
        function_body               : LBRACKET statement_list RBRACKET
        """
        self.eat(LBRACKET)
        node = Body(self.statement_list(allow_declaration=True))
        self.eat(RBRACKET)
        return node

    def var_declaration_list(self):
        """
        var_declaration_list        : type_spec var var_initialization (COMMA var var_initialization)* SEMICOLON
        """
        declarations = []

        type_node = self.type_spec()
        var_node = self.variable()

        declarations.extend(self.var_initialization(type_node, var_node))

        while self.current_token.type == COMMA:
            self.eat(COMMA)
            var_node = self.variable()
            declarations.extend(self.var_initialization(type_node, var_node))

        self.eat(SEMICOLON)

        return declarations

    def var_initialization(self, type_node, var_node):
        """
        var_initialization          : (ASSIGN expr)?
        """
        declarations = list()

        declarations.append(VarDecl(
            type_node=type_node,
            var_node=var_node
        ))

        if self.current_token.type == ASSIGN:
            token = self.current_token
            self.eat(ASSIGN)
            declarations.append(Assign(
                left=var_node,
                op=token,
                right=self.expr()
            ))
        return declarations

    def parameters(self):
        """
        parameters                  : empty
                                    | param
                                    | param COMMA parameters

        param                       : type_spec variable
        """

        if self.current_token.type == RPAREN:
            return []

        nodes = [Param(self.type_spec(), self.variable())]
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            nodes.append(Param(self.type_spec(), self.variable()))
        return nodes

    @restorable
    def check_function(self, declaration=False):
        """Look ahead to check declaration type"""
        if declaration:
            self.eat(TYPE)
        self.eat(ID)
        result = self.current_token.type == LPAREN
        return result

    def block(self):
        """
        block                       : LBRACKET statement_list RBRACKET
        """
        self.eat(LBRACKET)
        node = Block(self.statement_list())
        self.eat(RBRACKET)
        return node

    def statement_list(self, allow_declaration=False):
        """
        statement_list              : var_declaration_list
                                    | statement
                                    | statement statement_list
        """
        nodes = []

        while True:
            if self.current_token.type == TYPE and allow_declaration:
                nodes.extend(self.var_declaration_list())
            else:
                node = self.statement()
                if type(node) == NoOp:
                    break
                nodes.append(node)

        return nodes

    def statement(self):
        """
        statement                   : assignment_statement
                                    | if_statement
                                    | return_statement
                                    | empty
        """
        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == IF:
            node = self.if_statement()
        elif self.current_token.type == RETURN:
            node = self.return_statement()
        else:
            node = self.empty()
        return node

    def assignment_statement(self):
        """
        assignment_statement        : variable ASSIGN expr SEMICOLON
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN)
        node = Assign(left, token, self.expr())
        self.eat(SEMICOLON)
        return node

    def return_statement(self):
        """
        return_statement            : RETURN expr SEMICOLON
        """
        self.eat(RETURN)
        expr = self.expr()
        self.eat(SEMICOLON)
        return ReturnStmt(
            expr=expr
        )

    def if_statement(self):
        """
        if_statement                : IF LPAREN expr RPAREN stmt_body (ELSE stmt_body)?
        """
        self.eat(IF)
        self.eat(LPAREN)
        cond_node = self.expr()
        self.eat(RPAREN)
        if_body = self.stmt_body()
        else_body = self.empty()
        if self.current_token.type == ELSE:
            self.eat(ELSE)
            else_body = self.stmt_body()
        return IfStmt(
            condition=cond_node,
            if_body=if_body,
            else_body=else_body
        )

    def stmt_body(self):
        """
        stmt_body               : statement
                                | LBRACKET statement_list RBRACKET
        """
        if self.current_token.type == LBRACKET:
            self.eat(LBRACKET)
            node = Body(statements=self.statement_list())
            self.eat(RBRACKET)
        else:
            node = Body(statements=[self.statement()])
        return node

    def type_spec(self):
        """
        type_spec                   : TYPE
        """
        token = self.current_token
        self.eat(TYPE)
        node = Type(token)
        return node

    def variable(self):
        """
        variable                    : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def expr(self):
        """
        expr                        : term ((PLUS | MINUS) term)*
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def term(self):
        """
        term                        : factor ((MUL | DIV) factor)*
        """
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def factor(self):
        """
        factor                      : PLUS factor
                                    | MINUS factor
                                    | INT_NUMBER
                                    | LPAREN expr RPAREN
                                    | variable
        """
        token = self.current_token
        if token.type == PLUS:
            self.eat(PLUS)
            return UnaryOp(token, self.factor())
        elif token.type == MINUS:
            self.eat(MINUS)
            return UnaryOp(token, self.factor())
        elif token.type == INT_NUMBER:
            self.eat(INT_NUMBER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif self.check_function():
            return self.function_call()
        else:
            return self.variable()

    def function_call(self):
        """
        function_call               : ID LPAREN (expr)* RPAREN
        """
        func_name = self.current_token.value
        self.eat(ID)
        self.eat(LPAREN)
        params = []
        while self.current_token.type != RPAREN:
            params.append(self.expr())
            if self.current_token.type == COMMA:
                self.eat(COMMA)
        self.eat(RPAREN)
        return FunctionCall(
            func_name=func_name,
            params=params
        )

    def empty(self):
        """An empty production"""
        return NoOp()

    def parse(self):
        """
        program                     : declarations

        declarations                : (function_declaration | var_declaration_list)*

        function_declaration        : type_spec ID LPAREN parameters RPAREN function_body

        function_body               : LBRACKET statement_list RBRACKET

        var_declaration_list        : type_spec var var_initialization (COMMA var var_initialization)* SEMICOLON

        var_initialization          : (ASSIGN expr)?

        parameters                  : empty | param (COMMA param)*

        param                       : type_spec variable

        block                       : LBRACKET statement_list RBRACKET

        statement_list              : var_declaration_list
                                    | statement
                                    | statement statement_list

        statement                   : assignment_statement
                                    | if_statement
                                    | return_statement
                                    | empty

        assignment_statement        : variable ASSIGN expr SEMICOLON

        return_statement            : RETURN expr SEMICOLON

        if_statement                : IF LPAREN expr RPAREN stmt_body (ELSE stmt_body)?

        term                        : factor ((MUL | DIV) factor)*

        type_spec                   : TYPE

        variable                    : ID

        expr                        : term ((PLUS | MINUS) term)*

        term                        : factor ((MUL | DIV) factor)*

        factor                      : PLUS factor
                                    | MINUS factor
                                    | INT_NUMBER
                                    | LPAREN expr RPAREN
                                    | variable

        function_call               : ID LPAREN (expr)* RPAREN

        """

        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node
