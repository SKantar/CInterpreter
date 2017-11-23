import unittest

class LexerTestCase(unittest.TestCase):
    def makeParser(self, text):
        from interpreter.lexer import Lexer
        from interpreter.parser import Parser
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser

    def test_lexer_integer(self):
        parser = self.makeParser("""
            int main(a, int b){
                
            }
        """)
        parser.parse()