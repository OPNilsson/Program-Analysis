########################################################################################################################
#   Error:
#
#   This class is used when an error happens within the lexer
########################################################################################################################
from compiler.tokenTypes import Token, TT_PLUS, TT_EL, TT_METHOD, TT_MINUS, TT_MUL, TT_DIV, TT_POW, TT_L_PAREN, \
    TT_R_PAREN, TT_L_BRACKET, TT_R_BRACKET, TT_L_SQUARE, TT_R_SQUARE, TT_INT, TT_FLOAT, TT_KEYWORD, TT_IDENTIFIER, \
    TT_ASSIGN, TT_NE, TT_EQUALS, TT_EE, TT_LT, TT_LTE, TT_GTE, TT_GT, TT_STRING


class Error:

    def __init__(self, pos_start, pos_end, error_name, details):
        # keep track of where the error happened
        self.pos_start = pos_start
        self.pos_end = pos_end

        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f'{self.error_name}: {self.details}'
        result += f'\nFile: {self.pos_start.fn}, line {self.pos_start.ln + 1}'
        return result


class IllegalCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Illegal Character', details)


class ExpectedCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
    def __init__(self, pos_start, pos_end, details=''):
        super().__init__(pos_start, pos_end, 'Invalid Syntax', details)
