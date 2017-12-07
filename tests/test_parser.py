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


    def test_libraries(self):
        parser = self.makeParser("""
            #include <stdio.h>
            #include <stdlib.h>
            #include <math.h>
        """)
        parser.parse()

    def test_functions(self):
        parser = self.makeParser("""
           int main(){
           
           }
           
           int test(int a, int b){
                
           }
            
        """)
        parser.parse()

    def test_declarations(self):
        parser = self.makeParser("""
            int a, b = 2;
            int main(){
                int a, b = 3, c = 1 - b ++;
                a = a ^ b | b - 1 * 5 / (double)c - a++;
            }
        """)
        parser.parse()

    def test_function_call(self):
        parser = self.makeParser("""
            int a, b = 2;
            int main(){
                int a = printf("%d %d", b, c);
            }
        """)
        parser.parse()

    def test_if_stmt(self):
        parser = self.makeParser("""
            int a, b = 2;
            int main(){
                if(a = b)
                    b = 1;
                if(c == d | v)
                    a = 1;
                else
                    b = 1;
                    
                if(a == 1){
                    b = 1;
                    c = 1;
                }else{
                    c = 2;
                    e = 1;
                }  
                
                if(a == 1)
                    b = 1;
                else if (b == 1)
                    c = 5;  
                    
            }
        """)
        parser.parse()

    def test_for_stmt(self):
        parser = self.makeParser("""
            int a, b = 2;
            int main(){
                for(i = 0; i < n; i ++){
                    a = 1;
                }
                
                for(i = 1, b = 2; i > 1; i --){
                    b - 1;
                }
                
                for( i = 1, b = 2, c = 1; i < 1; i --, b++)
                    for(j = 0; j < 5; j ++)
                        for(;;){
                        
                        }

            }
        """)
        parser.parse()

    def test_while_do_stmt(self):
        parser = self.makeParser("""
            int a, b = 2;
            int main(){
                while(i < 1){
                    b = 1;
                }
                
                while(a > b)
                    while(b == 1){
                        a = 1;
                    }
                    
                do{
                    a = 1;
                }while(a < 5);

            }
        """)
        parser.parse()

