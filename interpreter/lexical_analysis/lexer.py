""" SCI - Simple C Interpreter """
from .token_type import *
from .token import Token

RESERVED_KEYWORDS = {
    'int': Token(TYPE, 'int'),
    'if': Token(IF, 'if'),
    'while': Token(WHILE, 'while'),
    'else': Token(ELSE, 'else'),
    'return': Token(RETURN, 'return'),
}


class LexicalError(Exception):
    pass


class Lexer(object):
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.line = 1

    def error(self, message='Invalid character'):
        raise LexicalError(message)

    def advance(self):
        """ Advance the `pos` pointer and set the `current_char` variable. """
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self):
        """ Check next char but don't change state. """
        peek_pos = self.pos + 1
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

    def integer(self):
        """ Return a (multidigit) integer consumed from the input. """
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        """ Return a (multidigit) integer consumed from the input. """
        result = ''
        self.advance()
        while self.current_char is not '"':
            if self.current_char is None:
                self.error(
                    message='Unfinished string with \'"\'at line {}'.format(self.line)
                )
            result += self.current_char
            self.advance()
        self.advance()
        return result

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

            if self.current_char.isalpha():
                return self._id()

            if self.current_char.isdigit():
                return Token(INT_NUMBER, self.integer())

            if self.current_char == '"':
                return Token(STRING, self.string())

            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LE, '<=')

            if self.current_char == '<':
                self.advance()
                return Token(LT, '<')

            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GE, '>=')

            if self.current_char == '>':
                self.advance()
                return Token(GT, '>')

            if self.current_char == '=' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(EQ, '==')

            if self.current_char == '=':
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == '!' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(NE, '!=')

            if self.current_char == '!':
                self.advance()
                return Token(NOT, '!')

            if self.current_char == '&' and self.peek() == '&':
                self.advance()
                self.advance()
                return Token(AND, '&&')

            if self.current_char == '&':
                self.advance()
                return Token(AMPERSAND, '&')

            if self.current_char == '|' and self.peek() == '|':
                self.advance()
                self.advance()
                return Token(OR, '||')

            if self.current_char == ';':
                self.advance()
                return Token(SEMICOLON, ';')

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

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

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '.':
                self.advance()
                return Token(DOT, '.')

            if self.current_char == '#':
                self.advance()
                return Token(HASH, '#')



            self.error(
                message="Invalid char {} at line {}".format(self.current_char, self.line)
            )

        return Token(EOF, None)
