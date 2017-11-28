import unittest


class InterpreterTestCase(unittest.TestCase):
    def interpret(self, text):
        from interpreter.interpreter.vm import Interpreter
        return Interpreter.run(text)

    def test_analyzer(self):
        print( self.interpret("""
            int test(int a){
                return a;
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
               
               return test(b + c + 3);
            }
        """))