# -*- coding: utf-8 -*-
import argparse
import textwrap

from compiler.lexer import Lexer
from compiler.parser import Parser, Traversal


class ASTVisualizer(Traversal):
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
        
    # def bfs(self, node):
    #     ncount = 1
    #     queue = []
    #     queue.append(node)
    #     s = '  node{} [label="{}"]\n'.format(ncount, node.name)
    #     self.dot_body.append(s)
    #     node._num = ncount
    #     ncount += 1

    #     while queue:
    #         node = queue.pop(0)
    #         for child_node in node.children:
    #             s = '  node{} [label="{}"]\n'.format(ncount, child_node.name)
    #             self.dot_body.append(s)
    #             child_node._num = ncount
    #             ncount += 1
    #             s = '  node{} -> node{}\n'.format(node._num, child_node._num)
    #             self.dot_body.append(s)
    #             queue.append(child_node)

    def visit_Integer(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_BinOp(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.operation.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit_node(node.left)
        self.visit_node(node.right)

        for child_node in (node.left, node.right):
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)
            
    def visit_UnaryOp(self, node):
        s = '  node{} [label="(1) {}"]\n'.format(self.ncount, node.operation.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit_node(node.expression)
        s = '  node{} -> node{}\n'.format(node._num, node.expression._num)
        self.dot_body.append(s)

    def gendot(self):
        tree = self.parser.parse()
        self.visit_node(tree)
        return ''.join(self.dot_header + self.dot_body + self.dot_footer)


    def visit_Compound(self, node):
        s = '  node{} [label="Scope"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit_node(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

    def visit_Assign(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.operation.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit_node(node.left)
        self.visit_node(node.right)

        for child_node in (node.left, node.right):
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)

    def visit_Variable(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_NoOp(self, node):
        s = '  node{} [label="NoOp"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        
    def visit_VariableDeclaration(self, node):
        s = '  node{} [label="VarDecl"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        
        self.visit_node(node.type_node)
        s = '  node{} -> node{}\n'.format(node._num, node.type_node._num)
        self.dot_body.append(s)


        # self.visit_node(node.var_node)
        # s = '  node{} -> node{}\n'.format(node._num, node.var_node._num)
        # self.dot_body.append(s)
        
        self.visit_node(node.assign_node)
        s = '  node{} -> node{}\n'.format(node._num, node.assign_node._num)
        self.dot_body.append(s)


    def visit_Type(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        
    def visit_ZeroNode(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1
        
    def visit_Record(self, node):
        s = '  node{} [label="Record"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit_node(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)
            
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

    def visit_Condition(self, node):
        s = '  node{} [label="{}"]\n'.format(self.ncount, node.operation.value)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        self.visit_node(node.left)
        self.visit_node(node.right)

        for child_node in (node.left, node.right):
            s = '  node{} -> node{}\n'.format(node._num, child_node._num)
            self.dot_body.append(s)




    def visit_If(self, node):
        s = '  node{} [label="If"]\n'.format(self.ncount)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

        for child in node.children:
            self.visit_node(child)
            s = '  node{} -> node{}\n'.format(node._num, child._num)
            self.dot_body.append(s)

        s = '  node{} [label="{}"]\n'.format(self.ncount, node.token)
        self.dot_body.append(s)
        node._num = self.ncount
        self.ncount += 1

def main():
    # argparser = argparse.ArgumentParser(
    #     description='Generate an AST DOT file.'
    # )
    # argparser.add_argument(
    #     'text',
    #     help='Arithmetic expression (in quotes): "1 + 2 * 3"'
    # )
    # args = argparser.parse_args()
    text = "{ int a; if(a > 1){ a:=10 } }"

    lexer = Lexer(text)
    parser = Parser(lexer)
    viz = ASTVisualizer(parser)
    content = viz.gendot()
    print(content)


if __name__ == '__main__':
    main()