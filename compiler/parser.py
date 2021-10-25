from compiler.lexer import Lexer
from compiler.static import *

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.token = self.operation = operation

class Integer(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):
    
    def __init__(self, lexer):
        self.lexer = lexer
        self.curr_token = self.lexer.get_next_token()
        
    def error(self):
        raise Exception('Invalid syntax')
        
    def consume(self, token_type):
        # look at the type of the current token and
        # compare it with the passed token type, if 
        # there is a match, consume the toke, otherwise
        # raise exception
        if self.curr_token.type == token_type: 
            self.curr_token = self.lexer.get_next_token()
        else:
            self.error()
            
    def parse_factor(self):
        token = self.curr_token
        
        if token.type == TT_INT:
            self.consume(TT_INT)
            return Integer(token)
        elif token.type == TT_L_PAREN:
            self.consume(TT_L_PAREN)
            node = self.parse_expression()
            self.consume(TT_R_PAREN)
            return node
        
        
    def parse_term(self):
        node = self.parse_factor()
        
        while self.curr_token.type in (TT_MUL, TT_DIV):
            token = self.curr_token
            if token.type == TT_MUL:
                self.consume(TT_MUL)
            elif token.type == TT_DIV:
                self.consume(TT_DIV)
                
            node = BinOp(left=node, right=self.parse_factor(), operation=token)
        return node
    
    def parse_expression(self):
        node = self.parse_term()
        
        while self.curr_token.type in (TT_PLUS, TT_MINUS):
            token = self.curr_token
            if token.type == TT_PLUS:
                self.consume(TT_PLUS)
            elif token.type == TT_MINUS:
                self.consume(TT_MINUS)
                
            node = BinOp(left=node, right=self.parse_term(), operation=token)
        
        return node
    
    def parse(self):
        return self.parse_expression()
    
class Traversal(object):
    
    def visit_node(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.visit_exception)
        return visitor(node)
    
    
    def visit_exception(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
        
    def visit_BinOp(self, node):
        if node.operation.type == PLUS:
            return self.visit_node(node.left) + self.visit_node(node.right)
        elif node.operation.type == MINUS:
            return self.visit_node(node.left) - self.visit_node(node.right)
        elif node.operation.type == MUL:
            return self.visit_node(node.left) * self.visit_node(node.right)
        elif node.operation.type == DIV:
            return self.visit_node(node.left) / self.visit_node(node.right)

    def visit_Integer(self, node):
        return node.value
# def main():
#     while True:
#         try:
#             ipt = input('microC> ')
#         except EOFError:
#             break
#         if not ipt:
#             continue
#     lexer = Lexer(ipt)
#     parser = Parser(lexer)
    
