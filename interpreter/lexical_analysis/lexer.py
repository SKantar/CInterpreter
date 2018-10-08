""" SCI - Simple C Interpreter """
from .token_type import *
from .token import Token

RESERVED_KEYWORDS = {
    'char': Token(CHAR, 'char'),
    'int': Token(INT, 'int'),
    'float': Token(FLOAT, 'float'),
    'double': Token(DOUBLE, 'double'),
    'if': Token(IF, 'if'),
    'else': Token(ELSE, 'else'),
    'for': Token(FOR, 'for'),
    'while': Token(WHILE, 'while'),
    'do': Token(DO, 'do'),
    'return': Token(RETURN, 'return'),
    'break': Token(BREAK, 'break'),
    'continue': Token(CONTINUE, 'continue'),
    'void': Token(VOID, 'void'),    
}


class LexicalError(Exception):
    """ Class was created to isolate lexical errors """
    pass


class Lexer(object):
    def __init__(self, text):
        self.text = text.replace('\\n', '\n')
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1

    def error(self, message):
        raise LexicalError(message)

    def advance(self):
        """ Advance the `pos` pointer and set the `current_char` variable. """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self, n):
        """ Check next n-th char but don't change state. """
        peek_pos = self.pos + n
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        """ Skip all whitespaces between tokens from input """
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def skip_comment(self):
        """ Skip single line comment """
        while self.current_char is not None:
            if self.current_char == '\n':
                self.line += 1
                self.advance()
                return
            self.advance()

    def skip_multiline_comment(self):
        """ Skip multi line comment """
        while self.current_char is not None:
            if self.current_char == '*' and self.peek(1) == '/':
                self.advance()
                self.advance()
                return
            if self.current_char == '\n':
                self.line += 1
            self.advance()
        self.error("Unterminated comment at line {}".format(self.line))

    def number(self):
        """Return a (multidigit) integer or float consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()

        if self.current_char == '.':
            result += self.current_char
            self.advance()

            while (self.current_char is not None and self.current_char.isdigit()):
                result += self.current_char
                self.advance()

            token = Token(REAL_CONST, float(result))
        else:
            token = Token(INTEGER_CONST, int(result))

        return token

    def string(self):
        """ Return string written in code without double quotes"""
        result = ''
        self.advance()
        while self.current_char is not '"':
            if self.current_char is None:
                self.error(
                    message='Unfinished string with \'"\' at line {}'.format(self.line)
                )
            result += self.current_char
            self.advance()
        self.advance()
        return Token(STRING, result)

    def char(self):
        """ Handle chars between single quotes """
        self.advance()
        char = self.current_char
        self.advance()
        if self.current_char != '\'':
            self.error("Unclosed char constant at line {}".format(self.line))
        self.advance()
        return Token(CHAR_CONST, ord(char))

    def _id(self):
        """ Handle identifiers and reserved keywords """
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()

        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token

    @property
    def get_next_token(self):
        """ Lexical analyzer (also known as scanner or tokenizer)
        This method is responsible for breaking a sentence
        apart into tokens. One token at a time. """

        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '/' and self.peek(1) == '/':
                self.skip_comment()
                continue

            if self.current_char == '/' and self.peek(1) == '*':
                self.skip_multiline_comment()
                continue

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return self.number()

            if self.current_char == '"':
                return self.string()

            if self.current_char == '\'':
                return self.char()

            if self.current_char == '<' and self.peek(1) == '<' and self.peek(2) == '=':
                self.advance()
                self.advance()
                self.advance()
                return Token(LEFT_ASSIGN, '<<=')

            if self.current_char == '>' and self.peek(1) == '>' and self.peek(2) == '=':
                self.advance()
                self.advance()
                self.advance()
                return Token(RIGHT_ASSIGN, '>>=')

            if self.current_char == '+' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(ADD_ASSIGN, '+=')

            if self.current_char == '-' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(SUB_ASSIGN, '-=')

            if self.current_char == '*' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(MUL_ASSIGN, '*=')

            if self.current_char == '/' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(DIV_ASSIGN, '/=')

            if self.current_char == '%' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(MOD_ASSIGN, '%=')

            if self.current_char == '&' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(AND_ASSIGN, '&=')

            if self.current_char == '^' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(XOR_ASSIGN, '^=')

            if self.current_char == '|' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(OR_ASSIGN, '|=')

            if self.current_char == '>' and self.peek(1) == '>':
                self.advance()
                self.advance()
                return Token(RIGHT_OP, '>>')

            if self.current_char == '<' and self.peek(1) == '<':
                self.advance()
                self.advance()
                return Token(LEFT_OP, '<<')

            if self.current_char == '+' and self.peek(1) == '+':
                self.advance()
                self.advance()
                return Token(INC_OP, '++')

            if self.current_char == '-' and self.peek(1) == '-':
                self.advance()
                self.advance()
                return Token(DEC_OP, '--')

            if self.current_char == '&' and self.peek(1) == '&':
                self.advance()
                self.advance()
                return Token(LOG_AND_OP, '&&')

            if self.current_char == '|' and self.peek(1) == '|':
                self.advance()
                self.advance()
                return Token(LOG_OR_OP, '||')

            if self.current_char == '<' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(LE_OP, '<=')

            if self.current_char == '>' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(GE_OP, '>=')

            if self.current_char == '=' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(EQ_OP, '==')

            if self.current_char == '!' and self.peek(1) == '=':
                self.advance()
                self.advance()
                return Token(NE_OP, '!=')

            if self.current_char == '<':
                self.advance()
                return Token(LT_OP, '<')

            if self.current_char == '>':
                self.advance()
                return Token(GT_OP, '>')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '!':
                self.advance()
                return Token(LOG_NEG, '!')

            if self.current_char == '&':
                self.advance()
                return Token(AND_OP, '&')

            if self.current_char == '|':
                self.advance()
                return Token(OR_OP, '|')

            if self.current_char == '^':
                self.advance()
                return Token(XOR_OP, '|')

            if self.current_char == '+':
                self.advance()
                return Token(ADD_OP, '+')

            if self.current_char == '-':
                self.advance()
                return Token(SUB_OP, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL_OP, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV_OP, '/')

            if self.current_char == '%':
                self.advance()
                return Token(MOD_OP, '%')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '{':
                self.advance()
                return Token(LBRACKET, '{')

            if self.current_char == '}':
                self.advance()
                return Token(RBRACKET, '}')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == ':':
                self.advance()
                return Token(COLON, ':')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')

            if self.current_char == '?':
                self.advance()
                return Token(QUESTION_MARK, '?')

            self.error(
                message="Invalid char {} at line {}".format(self.current_char, self.line)
            )

        return Token(EOF, None)
