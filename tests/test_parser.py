import unittest
from interpreter.lexical_analysis.lexer import Lexer
from interpreter.syntax_analysis.parser import Parser
from interpreter.syntax_analysis.parser import SyntaxError
from interpreter.syntax_analysis.tree import *

class LexerTestCase(unittest.TestCase):
    def makeParser(self, text):
        lexer = Lexer(text)
        parser = Parser(lexer)
        return parser

    def test_parser_function(self):
        parser = self.makeParser("""
            int main(){
                
            }
        """)
        tree = parser.parse()
        self.assertEqual(type(tree), Program)
        for child in tree.children:
            self.assertEqual(type(child), FunctionDecl)

    def test_parser_function_params(self):
        parser = self.makeParser("""
            int main(int a, int b){

            }
        """)
        parser.parse()
        tree = parser.parse()
        self.assertEqual(type(tree), Program)
        for func in tree.children:
            self.assertEqual(type(func), FunctionDecl)
            self.assertEqual(type(func.type_node), Type)
            self.assertEqual(func.type_node.value, 'int')
            self.assertEqual(func.func_name, 'main')
            for param in func.params:
                self.assertEqual(type(param), Param)
                self.assertEqual(type(param.type_node), Type)

    def test_parser_vars(self):
        parser = self.makeParser("""
            int a, b;
            int main(int a, int b){
                
            }
        """)
        tree = parser.parse()
        self.assertEqual(type(tree), Program)
        self.assertEqual(type(tree.children[0]), VarDecl)
        self.assertEqual(tree.children[0].var_node.value, 'a')
        self.assertEqual(tree.children[0].type_node.value, 'int')
        self.assertEqual(type(tree.children[1]), VarDecl)
        self.assertEqual(tree.children[1].var_node.value, 'b')
        self.assertEqual(tree.children[0].type_node.value, 'int')

    def test_parser_vars_with_assignment(self):
        parser = self.makeParser("""
            int a = 2, b = 2;
            int b;
            int main(int a, int b){

            }
        """)
        tree = parser.parse()
        self.assertEqual(type(tree), Program)
        self.assertEqual(type(tree.children[0]), VarDecl)
        self.assertEqual(tree.children[0].var_node.value, 'a')
        self.assertEqual(tree.children[0].type_node.value, 'int')
        self.assertEqual(type(tree.children[1]), Assign)
        self.assertEqual(tree.children[1].left.value, 'a')
        self.assertEqual(tree.children[1].right.value, 2)
        self.assertEqual(type(tree.children[2]), VarDecl)
        self.assertEqual(tree.children[2].var_node.value, 'b')
        self.assertEqual(tree.children[2].type_node.value, 'int')

    def test_parser_if(self):
        parser = self.makeParser("""
            int a = 2, b = 2;
            int b;
            int main(int a, int b){
                int a;
                a = 2 + 3;
                if(a + 2) {
                    a = 3 - 1;
                }
            }
        """)
        parser.parse()

    def test_parser_if_else(self):
        parser = self.makeParser("""
            int a = 2, b = 2;
            int b;
            int main(int a, int b){
                int a;
                a = 2 + 3;
                if(a + 2) {
                    a = 3 - 1;
                }else{
                    b = 2;
                }
                int a = 2;
                return 3;
            }
        """)
        parser.parse()

    def test_function_call(self):
        parser = self.makeParser("""
            int a = 2, b = 2;
            int b;

            int test(int a, int b){
                return a + b;
            }

            int main(int a, int b){
                int a;
                a = 2 + 3;
                if(a + 2) {
                    a = 3 - 1;
                }else{
                    b = 1;
                }
                return test(1, 3);
            }
        """)
        parser.parse()

    def test_include(self):
        parser = self.makeParser("""
            #include <stdio.h>
            int a = 2, b = 2;
            int b;
            
            int test(int a, int b){
                return a + b;
            }
            
            int main(int a, int b){
                int a;
                a = 2 + 3;
                if(a + 2) {
                    a = 3 - 1;
                }else{
                    b = 1;
                }
                test(1, 3);
                return 0;
            }
        """)
        parser.parse()

    def test_builtin_functions(self):
        parser = self.makeParser("""
            #include <stdio.h>
            int a = 2, b = 2;
            int b;

            int test(int a, int b){
                return a + b;
            }

            int main(int a, int b){
                int a;
                a = 2 + 3;
                scanf("%d", &a);
                if(a + 2) 
                    a = 3 - 1;
                else
                    b = 1;
                
                printf("%d", test(1, 3));
                return 0;
            }
        """)
        parser.parse()

    def test_error(self):
        parser = self.makeParser("""
            #include <stdio.h>
            int a = 2, b = 2;
            int b;

            int test(int a, int b){
                return a + b;
            }

            int main(int a, int b){
                int a;
                a = 2 + 3;
                scanf("%d", &a);
                if(a + 2) 
                    a = 3 - 1;
                    b = 2;
                else
                    b = 1;

                printf("%d", test(1, 3));
                return 0;
            }
        """)
        self.assertRaises(SyntaxError, parser.parse)