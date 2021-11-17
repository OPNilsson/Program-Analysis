from compiler.lexer import Lexer, Token


class AST(object):
    pass


class Compound(AST):
    # Represents a list of statement nodes
    def __init__(self):
        self.children = []


class Assign(AST):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.token = self.operation = operation


class ZeroNode(AST):
    def __init__(self):
        self.token = Token(TT_ZERO, '0')
        self.value = self.token.value


class Variable(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Type(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class NoOp(AST):
    pass


class VariableDeclaration(AST):
    def __init__(self, type_node, var_node):
        self.type_node = type_node
        self.var_node = var_node
        self.assign_node = Assign(self.var_node, ZeroNode(), Token(TT_ASSIGN, ':='))


class UnaryOp(AST):
    def __init__(self, operation, expression):
        self.token = self.operation = operation
        self.expression = expression


class BinOp(AST):
    def __init__(self, left, right, operation):
        self.left = left
        self.right = right
        self.token = self.operation = operation


class Record(AST):
    def __init__(self, children):
        self.children = children
        self.token = Token('R', 'R')


class Integer(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class Parser(object):

    def __init__(self, tokens):
        self.curr_token_index = 0
        self.tokens = tokens
        self.curr_token = tokens[0]

    def nextToken(self):
        self.curr_token_index = self.curr_token_index + 1
        self.curr_token = self.tokens[self.curr_token_index]
        
    def error(self):
        raise Exception('Invalid syntax')
        
    def consume(self, token_type):
        # look at the type of the current token and
        # compare it with the passed token type, if 
        # there is a match, consume the token, otherwise
        # raise exception
        # print(self.curr_token.type, token_type)
        if self.curr_token.type == token_type: 
            self.nextToken()
        else:
            print('consume error')
            self.error()
            
    def parse_factor(self):
        token = self.curr_token
        if token.type == TT_PLUS:
            self.consume(TT_PLUS)
            node = UnaryOp(token, self.parse_factor())
            return node
        elif token.type == TT_MINUS:
            self.consume(TT_MINUS)
            node = UnaryOp(token, self.parse_factor())
            return node
        elif token.type == TT_INT:
            self.consume(TT_INT)
            return Integer(token)
        elif token.type == TT_L_PAREN:
            self.consume(TT_L_PAREN)
            node = self.parse_expression()
            self.consume(TT_R_PAREN)
            return node
        else:
            node = self.parse_assign_statement()
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
        node = self.parse_program()
        if self.curr_token.type != TT_EOF and self.curr_token.type != TT_RECORD:
            print('parse error')
            self.error()
            
        return node
    
    def parse_program(self):
        # Set of Declarations and Statements
        return self.parse_compound_statement()
    
    def parse_compound_statement(self):
        self.consume(TT_L_BRACKET)
        nodes = self.parse_statement_list()
        self.consume(TT_R_BRACKET)
        
        root = Compound()
        for node in nodes:
            root.children.append(node)        
        return root
        
    def parse_statement_list(self):
        node = self.parse_statement()
        
        results = [node]
        
        while self.curr_token.type == TT_SEMI:
            self.consume(TT_SEMI)
            results.append(self.parse_statement())
        if self.curr_token.type == TT_IDENTIFIER:
            print('statement error')
            self.error()
        return results
        
    def parse_statement(self):
        # if self.curr_token.type == TT_L_BRACKET:
        #     node = self.parse_compound_statement()
        if self.curr_token.type == TT_IDENTIFIER:
            node = self.parse_assign_statement()
        elif self.curr_token.type == TT_VAR_TYPE:
            node = self.parse_variable_declaration()
        elif self.curr_token.type == TT_RECORD:
            node = self.parse_record()
        else:
            node = self.empty()
        return node
    
            
    def parse_assign_statement(self):
        left = self.parse_variable()
        token = self.curr_token
        self.consume(TT_ASSIGN)
        right = self.parse_expression()
        node = Assign(left, right, token) 
        return node

    
    def parse_variable(self):
        node = Variable(self.curr_token)
        self.consume(TT_IDENTIFIER)
        return node
    
    def parse_type(self):
        token = self.curr_token
        if token.type == TT_VAR_TYPE:
            self.consume(TT_VAR_TYPE)
        node = Type(token)
        return node
    
    def parse_variable_declaration(self):
        type_node = self.parse_type()
        var_node = self.parse_variable()
        declaration = VariableDeclaration(type_node, var_node)
        return declaration
    
    def empty(self):
        return NoOp()
    
    def parse_record(self):
        # self.consume(TT_L_BRACKET)
        nodes = self.parse_statement_list()
        # self.consume(TT_R_BRACKET)
        self.consume(TT_RECORD)
        self.consume(TT_SEMI)
        root = Record(nodes)
        # for node in nodes:
        #     root.children.append(node)        
        return root        
        
    
class Traversal(object):
    GLOBAL_SCOPE = {}
        
    def visit_node(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.visit_exception)
        return visitor(node)
    
    def visit_exception(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))
    
    def visit_UnaryOp(self, node):
        if node.operaion.type == TT_PLUS:
            return +self.visit_node(node.expression)
        if node.operaion.type == TT_MINUS:
            return -self.visit_node(node.expression)
        
    def visit_BinOp(self, node):
        if node.operation.type == TT_PLUS:
            return self.visit_node(node.left) + self.visit_node(node.right)
        elif node.operation.type == TT_MINUS:
            return self.visit_node(node.left) - self.visit_node(node.right)
        elif node.operation.type == TT_MUL:
            return self.visit_node(node.left) * self.visit_node(node.right)
        elif node.operation.type == TT_DIV:
            return self.visit_node(node.left) / self.visit_node(node.right)

    def visit_Integer(self, node):
        return node.value.value
    
    def visit_Compound(self, node):
        for child in node.children:
            self.visit_node(child)
    
    def visit_NoOp(self, node):
        pass
    
    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit_node(node.right)
    
    def visit_Variable(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val
        
    def visit_VariableDeclaration(self, node):
        # Do nothing
        pass

    def visit_Type(self, node):
        # Do nothing
        pass
    
    def visit_ZeroNode(self, node):
        # Do nothing
        pass
    
    def visit_Record(self, node):
        pass