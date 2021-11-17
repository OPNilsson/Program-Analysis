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