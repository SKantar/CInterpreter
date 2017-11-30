from interpreter.interpreter.interpreter import Interpreter
import argparse


parser = argparse.ArgumentParser(description='Execute .c file')
parser.add_argument('-f', '--file', help='File with C code')
parser.add_argument('-c', '--code', help='Code of C code')

args = parser.parse_args()
if not args.file and not args.code:
    argparse.ArgumentParser().error('You must choose one argument [-f or -c]')

elif args.file and args.code:
    argparse.ArgumentParser().error('You can choose only one argument [-f or -c]')

code = ''
if args.file:
    with open(args.file, 'r') as file:
        code = file.read()
else:
    code = args.code
Interpreter.run(code)
