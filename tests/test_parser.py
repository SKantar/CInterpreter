import unittest

class LexerTestCase(unittest.TestCase):
    def makeParser(self, text):
        from interpreter.lexer import Lexer
        from interpreter.parser import Parser
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser

    def test_parser_function(self):
        parser = self.makeParser("""
            int main(){
                
            }
        """)
        parser.parse()

    def test_parser_function_params(self):
        parser = self.makeParser("""
            int main(int a, int b){

            }
        """)
        parser.parse()

    def test_parser_vars(self):
        parser = self.makeParser("""
            int a, b;
            int main(int a, int b){

            }
        """)
        parser.parse()

    def test_parser_vars_with_assignment(self):
        parser = self.makeParser("""
            int a = 2, b = 2;
            int b;
            int main(int a, int b){

            }
        """)
        parser.parse()