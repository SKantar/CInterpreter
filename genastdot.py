###############################################################################
#  AST visualizer - generates a DOT file for Graphviz.                        #
#                                                                             #
#  To generate an image from the DOT file run $ dot -Tpng -o ast.png ast.dot  #
#                                                                             #
###############################################################################
import argparse
import textwrap

from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import NodeVisitor


class ASTVisualizer(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.ncount = 1
        self.dot_header = [textwrap.dedent("""\
        digraph astgraph {
          node [shape=circle, fontsize=12, fontname="Courier", height=.1];
          ranksep=.3;
          edge [arrowsize=.5]

        """)]
        self.dot_body = []
        self.dot_footer = ['}']

    def visit_Program(self, node):
        s = '  node{} [label="Program"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

    def visit_FunctionDecl(self, node):
        s = '  node{} [label="ProcDecl:{}"]\n'.format(
            self.ncount,
            node.func_name
        )
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for param_node in node.params:
            self.visit(param_node)
            s = '  node{} -> node{}\n'.format(node._num, param_node._num)
            self.dot_body.append(s)

    def visit_Param(self, node):
        s = '  node{} [label="Param"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit(node.var_node)
        s = '  node{} -> node{}\n'.format(node._num, node.var_node._num)
        self.dot_body.append(s)

        self.visit(node.type_node)
        s = '  node{} -> node{}\n'.format(node._num, node.type_node._num)
        self.dot_body.append(s)

    def visit_Type(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_Var(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def gendot(self):
        tree = self.parser.parse()
        self.visit(tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)


def main():
    argparser = argparse.ArgumentParser(
        description='Generate an AST DOT file.'
    )
    argparser.add_argument(
        'fname',
        help='Pascal source file'
    )
    args = argparser.parse_args()
    fname = args.fname
    text = open(fname, 'r').read()

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.gendot()
    print(content)


if __name__ == '__main__':
    main()
