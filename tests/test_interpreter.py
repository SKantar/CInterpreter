import unittest

class InterpreterTestCase(unittest.TestCase):
    def interpret(self, text):
        from interpreter.interpreter.interpreter import Interpreter
        return Interpreter.run(text)

    def test_analyzer(self):
        self.interpret("""
        #include <stdio.h>

        int main(){
            char d;
            char a, b, c;
    
            while((d = getchar()) != '\n'){
                if(d >= '0' && d <= '9'){
                    a = b;
                    b = c;
                    c = d;
                }
            }
            printf("%c%c%c", a, b, c);
            return 0;
        }

        """)