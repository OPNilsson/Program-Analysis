########################################################################################################################
#   Error:
#
#   This class is used when an error happens within the lexer
########################################################################################################################
import string
from compiler.static import *

########################################################################################################################
#   Tokens:
#
#   This class holds the categories (called TT or Token Types) for special characters that the lexer is interested in.
#
########################################################################################################################

class Token:
    def __init__(self, type, value=0):
        self.type = type
        self.value = value

        # if pos_start:
        #     self.pos_start = pos_start.copy()
        #     self.pos_end = pos_start.copy()
        #     self.pos_end.advance()

        # if pos_end:
        #     self.pos_end = pos_end


    # How the token is represented e.g. in console [type:value] || if no value [type]
    def __repr__(self):
        # if self.value:
        #     return f'{self.type}:{self.value}'

        # return f'{self.type}'
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )


########################################################################################################################
#   Lexer:
#
#   This class will look through the input txt in order to create a list of tokens that are recognized
#
#    This class was made following the tutorials :
#    https://www.youtube.com/watch?v=Eythq9848Fg & https://ruslanspivak.com/lsbasi-part7/
########################################################################################################################

# LETTERS = string.ascii_letters
# DIGITS = '0123465789'

# LETTERS_DIGITS = LETTERS + DIGITS

RESERVED_TOKENS = {
    '{': Token(TT_L_BRACKET, '{'),
    '}': Token(TT_R_BRACKET, '}'),
    'int': Token(TT_VAR_TYPE, 'int'),
    'float': Token(TT_VAR_TYPE, 'float'),
    'R': Token(TT_RECORD, 'R'),
    'if': Token(TT_IF, 'IF')
}


class Lexer:

    def __init__(self, micro_code_txt):
        self.text = micro_code_txt
        self.pos = 0
        self.current_char = self.text[self.pos]
        
    def error(self):
        string = f"Invalid character {self.current_char}"
        raise Exception(string)
        
    def make_id(self):
        # Handle identifiers and reserved tokens
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char in RESERVED_TOKENS.keys()):
            result += self.current_char
            self.advance()
            
        token = RESERVED_TOKENS.get(result, Token(TT_IDENTIFIER, result))
        return token

    # Advances one position in the text and sets the current_char
    def advance(self):
        # print(self.current_char)
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]
        # print(self.current_char)

            
    def peek_next(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text):
            return None
        else:
            return self.text[peek_pos]

            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
            
    def make_number(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def make_record(self):
        token = Token(TT_RECORD, 'R')
        self.make_id()
        while self.current_char is not None:    
            self.advance()
        return token
    
    def find_next_bracket(self):
        bracket_pos = self.pos
        while str(self.text).replace(' ', '')[bracket_pos] != '}':
            bracket_pos += 1
        return bracket_pos        
    
    def find_next_semi(self):
        pos = self.pos
        while str(self.text).replace(' ', '')[pos] != ';':
            pos += 1
        return pos
    
    def is_record(self):
        pos = self.pos
        is_record = False
        while str(self.text).replace(' ', '')[pos] != 'R':
            pos += 1
        else:
            is_record = True
        return is_record

    def is_if(self):
        pass


        
    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.current_char.isalpha() or self.current_char in RESERVED_TOKENS.keys():
                return self.make_id()
#                if self.current_char == '{' and self.is_record():
#                   return self.make_record()


            if self.current_char == ':' and self.peek_next() == '=':
                self.advance()
                self.advance()
                return Token(TT_ASSIGN, ':=')

            if self.current_char.isdigit():
                return Token(TT_INT, self.make_number())
            
            if self.current_char == ';':
                self.advance()
                return Token(TT_SEMI, ';')

            if self.current_char == '+':
                self.advance()
                return Token(TT_PLUS, '+')

            if self.current_char == '-':
                self.advance()
                return Token(TT_MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(TT_MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(TT_DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(TT_L_PAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(TT_R_PAREN, ')')

            self.error()

        return Token(TT_EOF, None)
    