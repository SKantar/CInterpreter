import unittest
from interpreter.lexical_analysis.token_type import *
from interpreter.lexical_analysis.lexer import LexicalError

class LexerTestCase(unittest.TestCase):
    def makeLexer(self, text):
        from interpreter.lexical_analysis.lexer import Lexer
        lexer = Lexer(text)
        return lexer

    def check(self, text, token_type, value=None):
        if not value:
            value = text
        lexer = self.makeLexer(text)
        token = lexer.get_next_token
        self.assertEqual(token.type, token_type)
        self.assertEqual(token.value, value)
        token = lexer.get_next_token
        self.assertEqual(token.type, EOF)

    def test_lexer_integer(self):
        self.check(
            text='234',
            token_type=INT_NUMBER,
            value=234
        )

    def test_lexer_mul(self):
        self.check(
            text='*',
            token_type=MUL
        )

    def test_lexer_div(self):
        self.check(
            text='/',
            token_type=DIV
        )

    def test_lexer_plus(self):
        self.check(
            text='+',
            token_type=PLUS
        )

    def test_lexer_minus(self):
        self.check(
            text='-',
            token_type=MINUS
        )

    def test_lexer_lparen(self):
        self.check(
            text='(',
            token_type=LPAREN
        )

    def test_lexer_rparen(self):
        self.check(
            text=')',
            token_type=RPAREN
        )

    def test_lexer_lbracket(self):
        self.check(
            text='{',
            token_type=LBRACKET
        )

    def test_lexer_rbracket(self):
        self.check(
            text='}',
            token_type=RBRACKET
        )

    def test_lexer_other_tokens(self):
        check_records = (
            ('=', ASSIGN, '='),
            ('name', ID, 'name'),
            ('int', TYPE, 'int'),
            (',', COMMA, ','),
            ('if', IF, 'if'),
            ('else', ELSE, 'else'),
            ('return', RETURN, 'return'),
            (';', SEMICOLON, ';'),
            (',', COMMA, ','),
            ('.', DOT, '.'),
            ('#', HASH, '#'),
            ('<', LT, '<'),
            ('<=', LE, '<='),
            ('>', GT, '>'),
            ('>=', GE, '>='),
            ('==', EQ, '=='),
            ('!=', NE, '!='),
            ('!', NOT, '!'),
            ('"String"', STRING, 'String'),
        )

        for text, tok_type, tok_val in check_records:
            self.check(
                text=text,
                token_type=tok_type,
                value=tok_val
            )

    def test_lexer_unexpected_char(self):
        lexer = self.makeLexer("@")
        with self.assertRaises(LexicalError) as le:
            test = lexer.get_next_token
        the_exception = le.exception
        self.assertEqual(str(the_exception), 'Invalid char @ at line 1')


