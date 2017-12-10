import unittest

class SemanticAnalyzerTestCase(unittest.TestCase):

    def analyze(self, text):
        from interpreter.lexical_analysis.lexer import Lexer
        from interpreter.syntax_analysis.parser import Parser
        from interpreter.semantic_analysis.analyzer import SemanticAnalyzer
        lexer = Lexer(text)
        parser = Parser(lexer)
        tree = parser.parse()
        SemanticAnalyzer.analyze(tree)

    def test_analyzer(self):
        self.analyze("""
            #include <stdio.h>
            #include <math.h>
            int a, b;
            int test(int a){
            
            }
            int main(int a){
                int b;
                int c = a + b;
                double d;
                scanf("%d %d", &a, &d);
                
                if(a + 5){
                    c = 2;
                }else{
                    b = 2;
                }
                
                int r = test(a);
                printf("%d", c + 2);
                return 0;
            }
            
        """)

    # def test_analyzer_with_error(self):
    #     self.analyze("""
    #         int a, b;
    #
    #         int main(int a){
    #
    #         }
    #     """)