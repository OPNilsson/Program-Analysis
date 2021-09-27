# #!/usr/bin/env python
# """parser.py: Parses Micro C language with the goal of creating http://www.formalmethods.dk/pa4fun/"""
# from stack import Stack


# # Checks two characters and returns whether they are a pair or not
# def __has_matching_pair(character1, character2):
#     if character1 == '(' and character2 == ')':
#         return True
#     elif character1 == '{' and character2 == '}':
#         return True
#     elif character1 == '[' and character2 == ']':
#         return True
#     else:
#         return False


# def __syntax_check(char_arr):

#     rules = {
#         "parentheses_open": ["(", "{", "["],
#         "parentheses_close": [")", "}", "]"],
#         "operators_arithmetic": ["+", "-", "*", "/", "%", "++", "--"],
#         "operators_relation": ["<", ">", "<=", ">=", "==", "!="],
#         "operators_logical": ["&&", "||", "!"]
#     }

#     # A stack is used to check for ordered pairs
#     # ex) { () } ✓  { ( } )  ✗
#     stack = Stack()

#     i = 0
#     while i < len(char_arr):

#         # An ending comment has been found
#         if char_arr[i] == '/' and char_arr[i + 1] == '*':
#             index = i
#             while index < len(char_arr):
#                 if char_arr[index] == '*' and char_arr[index + 1] == '/':
#                     i = index
#                     index = len(char_arr)
#                 index += 1

#         # If there is 2 '/' in a row then the line is a comment and doesn't need to be checked for syntax
#         if char_arr[i] == '/' and char_arr[i + 1] == '/':
#             return True

#         # If the arr[i] is a starting parenthesis then push it
#         if char_arr[i] == '{' or char_arr[i] == '(' or char_arr[i] == '[':
#             stack.push(char_arr[i])

#         # If arr[i] is an ending parenthesis then pop from stack
#         # check if the popped parenthesis is a matching pair
#         if char_arr[i] == '}' or char_arr[i] == ')' or char_arr[i] == ']':
#             # If we see an ending parenthesis without a pair then return false
#             if stack.isEmpty():
#                 return False

#             # Pop the top element from stack, if it is not a pair parenthesis of character then there is a mismatch.
#             elif not __has_matching_pair(stack.pop(), char_arr[i]):
#                 return False
#         i += 1

#     # If the stack is empty then there is a lose parentheses or comment starter
#     return stack.isEmpty()


# if __name__ == '__main__':
#     print("-------- Welcome to Micro C Parser --------")
#     code_str_arr = input("Enter a at least one line of code: ").replace(" ", "")

#     line_number = 0
#     colon_count = 0

#     # Counts ';' in code used for reference
#     for char in code_str_arr:
#         if ";" in char:
#             colon_count += 1

#     # Split the code into lines if more than one line
#     line_str_arr = code_str_arr.split(";")

#     # Loop through each line checking for syntax
#     # TODO: Keep track of all the errors not just break at error
#     for char_str_arr in line_str_arr:

#         # Don't check empty lines
#         if len(char_str_arr) != 0:

#             line_number += 1

#             print(line_number, "| ", char_str_arr)

#             # Last line is missing a ';'
#             if line_number <= colon_count:
#                 compiles =  __syntax_check(char_str_arr)

#                 if not compiles:
#                     print('Line ', line_number, " Error!")

#             else:
#                 print('Expected ";" at line ', line_number)
#                 break

from parserFolder.ast import BinOp

# STATIC VALUES
INTEGER = 'INTEGER'
PLUS, MINUS = ('PLUS', 'MINUS')
MUL, DIV = ('MUL', 'DIV')
LPAR, RPAR = ('(', ')')
EOF = 'EOF'


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
            self.curr_token == self.lexer.get_next_token()
        else:
            self.error()
            
    def parse_factor(self):
        token = self.curr_token
        
        if token.type == INTEGER:
            self.consume(INTEGER)
        elif token.type == LPAR:
            self.consume(LPAR)
            node = self.parse_expression()
            self.consume(RPAR)
            return node
        
        
    def parse_term(self):
        node = self.parse_factor()
        
        while self.curr_token.type in (MUL, DIV):
            token = self.curr_token
            if token.type == MUL:
                self.consume(MUL)
            elif token.type == DIV:
                self.consume(DIV)
                
            node = BinOp(left=node, right=self.parse_factor(), token=token)
            
    def parse_expression(self):
        node = self.parse_term()
        
        while self.curr_token.type in (PLUS, MINUS):
            token = self.curr_token
            if token.type == PLUS:
                self.consume(PLUS)
            elif token.type == MINUS:
                self.consume(MINUS)
                
            node = BinOp(left=node, right=self.term(), token=token)
        
        return node
    
class Traversal(object):
    
    def visit_node(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.visit_error)
        return visitor(node)
    
    
    def visit_error(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))



