########################################################################################################################
#   Tokens:
#
#   This class holds the categories (called TT or Token Types) for special characters that the lexer is interested in.
#
########################################################################################################################

# Data Types
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'
TT_STRING = 'STRING'
TT_RECORD = 'RECORD'

# Variable
TT_VAR_INT = 'VAR_INT'
TT_VAR_TYPE = 'VAR_TYPE'

# Arithmetic
TT_PLUS = 'PLUS'  # +
TT_MINUS = 'MINUS'  # -
TT_MUL = 'MUL'  # *
TT_DIV = 'DIV'  # /
TT_POW = 'POW'  # ^
TT_EQUALS = 'EQUALS'  # =

# Pairs
TT_L_PAREN = 'L_PAREN'  # (
TT_R_PAREN = 'R_PAREN'  # )
TT_L_BRACKET = 'L_BRACKET'  # {
TT_R_BRACKET = 'R_BRACKET'  # }
TT_L_SQUARE = 'L_SQUARE'  # [
TT_R_SQUARE = 'R_SQUARE'  # ]

# Specials
TT_IDENTIFIER = 'IDENTIFIER'  # name of int or var (ie: var IDENTIFIER = 2)
TT_KEYWORD = 'KEYWORD'  # var || int || words found in KEYWORDS
TT_METHOD = 'METHOD'  # .
TT_EL = 'EL'  # ;
TT_EOF = 'EOF' # an indicator that it is the end of the file

# Comparators and logical operators
TT_ASSIGN = 'ASSIGN'    # :=
TT_EE = 'EE'  # ==
TT_NE = 'NE'  # !=
TT_LT = 'LT'  # <
TT_GT = 'GT'  # >
TT_LTE = 'LTE'  # <=
TT_GTE = 'GTE'  # >=

TT_ZERO = '0'
TT_SEMI = 'SEMI' # ;


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        self.pos_start = pos_start
        self.pos_end = pos_end

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    # checks if the token matches the given type and value
    def matcher(self, type_, value):
        return self.type == type_ and self.value == value

    # How the token is represented e.g. in console [type:value] || if no value [type]
    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'

        return f'{self.type}'