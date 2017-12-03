import unittest
from interpreter.lexical_analysis.lexer import Lexer
from interpreter.syntax_analysis.parser import Parser
from interpreter.syntax_analysis.parser import SyntaxError
from interpreter.syntax_analysis.tree import *

class ParserTestCase(unittest.TestCase):
    def makeParser(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser

    # def test_conditional_function(self):
    #     parser = self.makeParser("""
    #         a = b = c = !a + 5 + 5 ^ 1;
    #     """)
    #     parser.parse()
    #
    # def test_cast_function(self):
    #     parser = self.makeParser("""
    #         a = (int)a;
    #     """)
    #     parser.parse()
    #
    # def test_inc_dec_function(self):
    #     parser = self.makeParser("""
    #         b = ++a - --b;
    #     """)
    #     parser.parse()
    #
    # def test_expr_function(self):
    #     parser = self.makeParser("""
    #         !a + 5 + 5 ^ 1;
    #     """)
    #     parser.parse()

    def test_stmt_function(self):
        parser = self.makeParser("""
            int main(){
                int a = c = 1 + 2, b = 3 + 3, c;
            
                if(a < 5){
                    a = 2;
                }else{
                    b = 3;
                }
                
                for(i = 0, i = 2; ; ){
                    a = 2;
                }
                
                return a + b;
                
                return a < b ? b : a;
            }
            
        """)
        parser.parse()

