import unittest

class LexerTestCase(unittest.TestCase):
    def makeLexer(self, text):
        from interpreter.lexer import Lexer
        lexer = Lexer(text)
        return lexer

    def test_lexer_integer(self):
        from interpreter.lexer import INT_NUMBER
        lexer = self.makeLexer('234')
        token = lexer.get_next_token()
        self.assertEqual(token.type, INT_NUMBER)

        self.assertEqual(token.value, 234)

    def test_lexer_mul(self):
        from interpreter.lexer import MUL
        lexer = self.makeLexer('*')
        token = lexer.get_next_token()
        self.assertEqual(token.type, MUL)

        self.assertEqual(token.value, '*')

    def test_lexer_div(self):
        from interpreter.lexer import DIV
        lexer = self.makeLexer(' / ')
        token = lexer.get_next_token()
        self.assertEqual(token.type, DIV)
        self.assertEqual(token.value, '/')

    def test_lexer_plus(self):
        from interpreter.lexer import PLUS
        lexer = self.makeLexer('+')
        token = lexer.get_next_token()
        self.assertEqual(token.type, PLUS)
        self.assertEqual(token.value, '+')

    def test_lexer_minus(self):
        from interpreter.lexer import MINUS
        lexer = self.makeLexer('-')
        token = lexer.get_next_token()
        self.assertEqual(token.type, MINUS)
        self.assertEqual(token.value, '-')

    def test_lexer_lparen(self):
        from interpreter.lexer import LPAREN
        lexer = self.makeLexer('(')
        token = lexer.get_next_token()
        self.assertEqual(token.type, LPAREN)
        self.assertEqual(token.value, '(')

    def test_lexer_rparen(self):
        from interpreter.lexer import RPAREN
        lexer = self.makeLexer(')')
        token = lexer.get_next_token()
        self.assertEqual(token.type, RPAREN)

        self.assertEqual(token.value, ')')

    def test_lexer_new_tokens(self):
        from interpreter.lexer import ASSIGN, ID, TYPE, COMMA, SEMICOLON
        records = (
            ('=', ASSIGN, ':='),
            ('number', ID, 'number'),
            ('int', TYPE, 'int'),
            (',', COMMA, ','),
            (';', SEMICOLON, ';'),
        )

        for text, tok_type, tok_val in records:
            lexer = self.makeLexer(text)
            token = lexer.get_next_token()
            self.assertEqual(token.type, tok_type)

        self.assertEqual(token.value, tok_val)


