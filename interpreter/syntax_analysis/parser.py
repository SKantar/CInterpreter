""" SCI - Simple C Interpreter """

from ..lexical_analysis.token_type import *
from .tree import *
from ..utils.utils import restorable

class SyntaxError(Exception):
    pass


class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token  # set current token to the first token taken from the input

    def error(self, message):
        raise SyntaxError(message)

    def eat(self, token_type):
        """ Compare the current token type with the passed token
        type and if they match then "eat" the current token
        and assign the next token to the self.current_token,
        otherwise raise an exception. """

        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token
        else:
            self.error(
                'Expected token <{}> but found <{}> at line {}.'.format(
                    token_type, self.current_token.type, self.lexer.line
                )
            )

    def program(self):
        """
        program                     : declarations
        """
        root = Program(self.declarations())
        return root

    def declarations(self):
        """
        declarations                : (include_library | function_declaration | var_declaration_list)*
        """
        declarations = []

        while self.current_token.type in [FLOAT, DOUBLE, INT, HASH]:
            if self.current_token.type == HASH:
                declarations.append(self.include_library())
            elif self.check_function():
                declarations.append(self.function_declaration())
            else:
                declarations.extend(self.declaration_list())
        return declarations

    def include_library(self):
        """
        include_library             : HASH ID<'include'> LESS_THAN ID DOT ID<'h'> GREATER_THAN
        """
        self.eat(HASH)
        token = self.current_token
        if token.value != 'include':
            self.error(
                'Expected token "include" but found {} at line {}.'.format(
                    token.value, self.lexer.line
                )
            )

        self.eat(ID)
        self.eat(LT_OP)
        token = self.current_token
        self.eat(ID)
        self.eat(DOT)
        extension = self.current_token
        if extension.value != 'h':
            self.error(
                'You can include only *.h files [line {}]'.format(self.lexer.line)
            )
        self.eat(ID)
        self.eat(GT_OP)
        return IncludeLibrary(
            library_name=token.value
        )

    @restorable
    def check_function(self):
        self.eat(self.current_token.type)
        self.eat(ID)
        return self.current_token.type == LPAREN

    def function_declaration(self):
        """
        function_declaration        : type_spec ID LPAREN parameters RPAREN block
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
            body=self.compound_statement()
        )

    def parameters(self):
        """
        parameters                  : empty
                                    | type_spec variable (COMMA type_spec variable)*
        """
        nodes = []
        if self.current_token.type != RPAREN:
            nodes = [Param(self.type_spec(), self.variable())]
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                nodes.append(Param(self.type_spec(), self.variable()))
        return nodes

    def declaration_list(self):
        result = [self.declaration()]
        while self.current_token.type == (INT, FLOAT, DOUBLE):
            result.append(self.declaration())
        return result

    def declaration(self):
        result = list()
        type_node = self.type_spec()
        for node in self.init_declarator_list():
            if isinstance(node, Var):
                result.append(VarDecl(
                    type_node=type_node,
                    var_node=node
                ))
            else:
                result.append(node)
        self.eat(SEMICOLON)
        return result

    def init_declarator_list(self):
        result = list()
        result.append(self.init_declarator())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            result.extend(self.init_declarator())
        return result

    def init_declarator(self):
        var = self.variable()
        result = list()
        result.append(var)
        if self.current_token.type == ASSIGN:
            token = self.current_token
            self.eat(ASSIGN)
            result.append(Assign(left=var, op=token, right=self.assignment_expression()))
        return result

    def statement(self):
        if self.check_iteration_statement():
            return self.iteration_statement()
        elif self.check_selection_statement():
            return self.selection_statement()
        elif self.check_jump_statement():
            return self.jump_statement()
        elif self.check_compound_statement():
            return self.compound_statement()
        return self.expression_statement()

    def check_compound_statement(self):
        return self.current_token.type == LBRACKET

    def compound_statement(self):
        result = []
        self.eat(LBRACKET)
        while self.current_token.type != RBRACKET:
            if self.current_token.type in (INT, FLOAT, DOUBLE):
                result.extend(self.declaration_list())
            else:
                result.append(self.statement())
        self.eat(RBRACKET)
        return CompoundStmt(
            children=result
        )

    def check_jump_statement(self):
        return self.current_token.type in (RETURN, BREAK, CONTINUE)

    def jump_statement(self):
        if self.current_token.type == RETURN:
            self.eat(RETURN)
            expression = NoOp()
            if self.current_token.type != SEMICOLON:
                expression = self.expression()
            return ReturnStmt(
                expression = expression
            )
        elif self.current_token.type == BREAK:
            self.eat(BREAK)
            self.eat(SEMICOLON)
            return BreakStmt()

        elif self.current_token.type == CONTINUE:
            self.eat(CONTINUE)
            self.eat(SEMICOLON)
            return BreakStmt()

    def check_selection_statement(self):
        return self.current_token.type == IF

    def selection_statement(self):
        if self.current_token.type == IF:
            self.eat(IF)
            self.eat(LPAREN)
            condition = self.expression()
            self.eat(RPAREN)
            tstatement = self.statement()
            fstatement = NoOp()
            if self.current_token.type == ELSE:
                self.eat(ELSE)
                fstatement = self.statement()
            return IfStmt(
                condition=condition,
                tbody=tstatement,
                fbody=fstatement
            )
        # TODO: Switch

    def check_iteration_statement(self):
        return self.current_token.type in (WHILE, DO, FOR)

    def iteration_statement(self):
        if self.current_token.type == WHILE:
            self.eat(WHILE)
            self.eat(LPAREN)
            expression = self.expression()
            self.eat(RPAREN)
            statement = self.statement()
            return WhileStmt(
                condition=expression,
                body=statement
            )
        elif self.current_token.type == DO:
            self.eat(DO)
            statement = self.statement()
            self.eat(WHILE)
            self.eat(LPAREN)
            expression = self.expression()
            self.eat(RPAREN)
            return DoWhileStmt(
                condition=expression,
                body=statement
            )
        else:
            self.eat(FOR)
            self.eat(LPAREN)
            setup = self.expression_statement()
            condition = self.expression_statement()
            increment = NoOp()
            if self.current_token.type != RPAREN:
                increment = self.expression()
            self.eat(RPAREN)
            statement = self.statement()
            return ForStmt(
                setup=setup,
                condition=condition,
                increment=increment,
                body=statement
            )

    def expression_statement(self):
        node = None
        if self.current_token.type != SEMICOLON:
            node = self.expression()
        self.eat(SEMICOLON)
        return node and node or NoOp()

    def constant_expression(self):
        return self.conditional_expression()

    def expression(self):
        result = list()
        result.append(self.assignment_expression())
        while self.current_token.type == COMMA:
            self.eat(COMMA)
            result.append(self.assignment_expression())
        return Expression(
            children=result
        )

    @restorable
    def check_assignment_expression(self):
        if self.current_token.type == ID:
            self.eat(ID)
            return self.current_token.type.endswith('ASSIGN')
        return False

    def assignment_expression(self):
        if self.check_assignment_expression():
            node = self.variable()
            while self.current_token.type.endswith('ASSIGN'):
                token = self.current_token
                self.eat(token.type)
                return Assign(
                    left=node,
                    op=token,
                    right=self.assignment_expression()
                )
        return self.conditional_expression()

    def conditional_expression(self):
        node = self.logical_and_expression()
        if self.current_token.type == QUESTION_MARK:
            self.eat(QUESTION_MARK)
            texpression = self.expression()
            self.eat(COLON)
            fexpression = self.conditional_expression()
            return TerOp(condition=node, texpression=texpression, fexpression=fexpression)
        return node

    def logical_and_expression(self):
        node = self.logical_or_expression()
        while self.current_token.type == LOG_AND_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.logical_or_expression())
        return node

    def logical_or_expression(self):
        node = self.inclusive_or_expression()
        while self.current_token.type == LOG_OR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.inclusive_or_expression())
        return node

    def inclusive_or_expression(self):
        node = self.exclusive_or_expression()
        while self.current_token.type == OR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.exclusive_or_expression())
        return node

    def exclusive_or_expression(self):
        node = self.and_expression()
        while self.current_token.type == XOR_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.and_expression())
        return node

    def and_expression(self):
        node = self.equality_expression()
        while self.current_token.type == AND_OP:
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.equality_expression())
        return node

    def equality_expression(self):
        node = self.relational_expression()
        if self.current_token.type in (EQ_OP, NE_OP):
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.relational_expression())
        return node

    def relational_expression(self):
        """
        logic_expr                  : arithm_expr ((LE | LT | GE | GT) arithm_expr)?
        """
        node = self.shift_expression()
        if self.current_token.type in (LE_OP, LT_OP, GE_OP, GT_OP):
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.shift_expression())
        return node

    def shift_expression(self):
        node = self.additive_expression()
        if self.current_token.type in (LEFT_OP, RIGHT_OP):
            token = self.current_token
            self.eat(token.type)
            return BinOp(left=node, op=token, right=self.additive_expression())
        return node

    def additive_expression(self):
        """
        arithm_expr                 : term ((PLUS | MINUS) term)*
        """
        node = self.multiplicative_expression()

        while self.current_token.type in (ADD_OP, SUB_OP):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.multiplicative_expression())

        return node

    def multiplicative_expression(self):
        """
        term                        : factor ((MUL | DIV) factor)*
        """
        node = self.cast_expression()
        while self.current_token.type in (MUL_OP, DIV_OP, MOD_OP):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.cast_expression())
        return node

    @restorable
    def check_cast_expression(self):
        if self.current_token.type == LPAREN:
            self.eat(LPAREN)
            if self.current_token.type in [DOUBLE, INT, FLOAT]:
                self.eat(self.current_token.type)
                return self.current_token.type == RPAREN
        return False

    def cast_expression(self):
        if self.check_cast_expression():
            self.eat(LPAREN)
            type_node = self.type_spec()
            self.eat(RPAREN)
            return UnOp(type_node, self.cast_expression())
        else:
            return self.unary_expression()

    def unary_expression(self):
        if self.current_token.type in (INC_OP, DEC_OP):
            token = self.current_token
            self.eat(token.type)
            return UnOp(token, self.unary_expression())
        elif self.current_token.type in (AND_OP, ADD_OP, SUB_OP, LOG_NEG):
            token = self.current_token
            self.eat(token.type)
            return UnOp(token, self.cast_expression())
        else:
            return self.postfix_expression()

    def postfix_expression(self):
        node = self.primary_expression()
        if self.current_token.type in (INC_OP, DEC_OP):
            token = self.current_token
            self.eat(token.type)
            node = UnOp(token, node, prefix=False)
        elif self.current_token.type == LPAREN:
            self.eat(LPAREN)
            args = list()
            if not self.current_token.type == RPAREN:
                args = self.argument_expression_list()
            node = FunctionCall(
                name=node,
                args=args
            )
        return node

    def argument_expression_list(self):
        args = [self.assignment_expression()]
        while self.current_token.type == COMMA:
            args.append(self.assignment_expression())
        return args

    def primary_expression(self):
        token = self.current_token
        if token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expression()
            self.eat(RPAREN)
            return node
        elif token.type in (INTEGER_CONST, REAL_CONST):
            return self.constant()
        elif token.type == STRING:
            return self.string()
        else:
            return self.variable()

    def constant(self):
        token = self.current_token
        if token.type == INTEGER_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)
        elif token.type == REAL_CONST:
            self.eat(INTEGER_CONST)
            return Num(token)

    def type_spec(self):
        """
        type_spec                   : TYPE
        """
        token = self.current_token
        if token.type in (INT, FLOAT, DOUBLE):
            self.eat(token.type)
            return Type(token)

    def variable(self):
        """
        variable                    : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def function_call(self):
        """
        function_call               : ID LPAREN RPAREN
                                    | ID LPAREN call_param (COMMA call_param)* RPAREN
        """
        func_name = self.current_token.value
        params = list()
        self.eat(ID)
        self.eat(LPAREN)
        if self.current_token.type != RPAREN:
            params.append(self.call_param())
            while self.current_token.type == COMMA:
                self.eat(COMMA)
                params.append(self.call_param())
        self.eat(RPAREN)
        return FunctionCall(
            func_name=func_name,
            params=params
        )

    def call_param(self):
        if self.current_token.type == STRING:
            return self.string()
        else:
            return self.expr()

    def string(self):
        """
        string                      : STRING
        """
        token = self.current_token
        self.eat(STRING)
        return String(token)

    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error("Expected token <EOF> but found <{}>".format(self.current_token.type))

        return node
