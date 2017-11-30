import unittest


class InterpreterTestCase(unittest.TestCase):
    def interpret(self, text):
        from interpreter.interpreter.vm import Interpreter
        return Interpreter.run(text)

    def test_analyzer(self):
        self.interpret("""
            #include <stdio.h>
            int test(int a){
                printf("%d", a);
            }
            int b = 1 + 2;

            int main(){
               int a = 2;
               int c = a + 3 - 1;
               if(5){
                    c = 1;
                    c = c + 1; 
               }
               else
               {
                    c = -2;
               }
               printf("%.2f", test(b + c + 3));
               return 0;
            }
        """)