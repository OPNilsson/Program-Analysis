import textwrap

import graphviz
from compiler.tokenTypes import Token, TT_PLUS, TT_EL, TT_METHOD, TT_MINUS, TT_MUL, TT_DIV, TT_POW, TT_L_PAREN, \
    TT_R_PAREN, TT_L_BRACKET, TT_R_BRACKET, TT_L_SQUARE, TT_R_SQUARE, TT_INT, TT_FLOAT, TT_KEYWORD, TT_IDENTIFIER, \
    TT_ASSIGN, TT_NE, TT_EQUALS, TT_EE, TT_LT, TT_LTE, TT_GTE, TT_GT, TT_STRING, TT_EOF

########################################################################################################################
#   Interpreter:
#
#   This class will read the tree input and interpret what each node represents
#   The input is called "node" because the tree itself will have a base node type
#
#    This class was made following the tutorials:
#    https://www.youtube.com/watch?v=Eythq9848Fg & https://ruslanspivak.com/lsbasi-part7/
#
#   This class is the one that least resembles the tutorials as the compiler was not needed for this course
#   all implementations of the tutorial are only loosely done as the result of this version is not the compiled result
#   instead the result of this interpreter will be a multi dimension array containing each node creating a AST
########################################################################################################################

class Interpreter:

    def __init__(self):
        self.index = 0

        self.graph = graphviz.Digraph('AST', filename='ast.gv')

        # Initial setup of the dot file
        self.graph.node_attr ={
            'shape': 'circle',
            'fontsize': '12',
            'fontname': 'Courier'
        }

        self.graph.edge_attr = {
            'arrowsize': '.5'
        }

        # In case you don't want it to be in a pdf file
        # self.graph.format = 'svg'

    def view_tree(self):
        self.graph.view()

    def visit(self, node):
        # Determine what type of method the node was
        method_name = f'visit_{type(node).__name__}'

        # The method that should be called
        # no_visit_method is the default
        method = getattr(self, method_name, self.no_visit_method)
        return method(node)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    def visit_NumberNode(self, node):
        # Increase the index of the node
        self.index = self.index + 1

        # Turn the int into a string
        number = str(node.tok.value)

        # Append the node to the graph with name of index and label of
        self.graph.node(self.index.__str__(), number)

        # used by other methods such as the UnaryOp
        return self.index

    def visit_UnaryOpNode(self, node):
        # Increase the index of the node
        self.index = self.index + 1

        # visit its child to get the number
        number = str(node.node.tok.value)

        if node.op_tok.type == TT_MINUS:
            operator_symbol = '-'
        elif node.op_tok.type == TT_PLUS:
            operator_symbol = '+'

        label = operator_symbol + number

        # Append the node to the graph with name of index and label of the sign and number
        self.graph.node(self.index.__str__(), label)



    def visit_BinOpNode(self, node):
        # Reformat the node


        # Increase the index of the node
        self.index = self.index + 1

        # turn the TT of the operator into a string
        if node.op_tok.type == TT_PLUS:
            operator_symbol = '+'
        elif node.op_tok.type == TT_MINUS:
            operator_symbol = '-'
        elif node.op_tok.type == TT_MUL:
            operator_symbol = '*'
        elif node.op_tok.type == TT_DIV:
            operator_symbol = 'C3B7'
        elif node.op_tok.type == TT_POW:
            operator_symbol = '^'
        elif node.op_tok.type == TT_EE:
            operator_symbol = '=='
        elif node.op_tok.type == TT_NE:
            operator_symbol = '!='
        elif node.op_tok.type == TT_LT:
            operator_symbol = '<'
        elif node.op_tok.type == TT_GT:
            operator_symbol = '>'
        elif node.op_tok.type == TT_LTE:
            operator_symbol = '<='
        elif node.op_tok.type == TT_GTE:
            operator_symbol = '>='

        # Append the node to the graph with name of index and label of operator
        self.graph.node(self.index.__str__(), operator_symbol)

        # Check what the child nodes are
        left = self.visit(node.left_node)
        right = self.visit(node.right_node)

        # Append the child nodes to the graph

########################################################################################################################
#   InterpretedNodes:
#
#   This class reformat all the nodes classes from the parser into being a single object with type, value, children
########################################################################################################################

class InterpretedNode:
    def __init__(self, parent, left_child, right_child, node_type, value):
        self.parent = parent
        self.leftChild = left_child
        self.rightChild = right_child
        self.node_type = node_type
        self.value = value
