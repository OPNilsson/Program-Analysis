########################################################################################################################
#   Error:
#
#   This class is used when an error happens within the lexer
########################################################################################################################
import string


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


########################################################################################################################
#   Position:
#
#   This class is used to keep track of where the lexer is looking at.
#
########################################################################################################################

class Position:
    def __init__(self, idx, ln, col, fn):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn  # filename of current file

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn)


########################################################################################################################
#   Tokens:
#
#   This class holds the categories (called TT or Token Types) for special characters that the lexer is interested in.
#
########################################################################################################################


# Variables
TT_INT = 'INT'
TT_FLOAT = 'FLOAT'

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

# Specials
TT_IDENTIFIER = 'IDENTIFIER'  # name of int or var (ie: var IDENTIFIER = 2)
TT_KEYWORD = 'KEYWORD'  # var || int

# Comparators and logical operators
TT_EE = 'EE'  # ==
TT_NE = 'NE'  # !=
TT_LT = 'LT'  # <
TT_GT = 'GT'  # >
TT_LTE = 'LTE'  # <=
TT_GTE = 'GTE'  # >=

KEYWORDS = [
    'int',
    'read',
    'write'
]


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

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


########################################################################################################################
#   Lexer:
#
#   This class
#
#    This class was made following the tutorials :
#    https://www.youtube.com/watch?v=Eythq9848Fg & https://ruslanspivak.com/lsbasi-part7/
########################################################################################################################

LETTERS = string.ascii_letters
DIGITS = '0123465789'

LETTERS_DIGITS = LETTERS + DIGITS


class Lexer:

    def __init__(self, filename, micro_code_txt):
        self.text = micro_code_txt
        self.fn = filename

        # The current position and character that the lexer is looking at
        # pos starts at -1 because the lexer immediately advances a position when constructed
        self.pos = Position(-1, 0, -1, self.fn)
        self.current_char = None

        self.advance()

    # Advances one position in the text and sets the current_char
    def advance(self):
        # is the same as self.pos += 1 but using custom position object to keep track of line and col
        self.pos.advance(self.current_char)

        # Sets the current character equal to that of the position unless it's the end of the text
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    # Assigns the current char to a Token and appends it to the tokens list
    def make_tokens(self):
        token_list = []

        # While the currentChar is not the end of the text
        while self.current_char is not None:

            # ignore spaces and tabs
            if self.current_char in ' \t':
                self.advance()

            # check if it's a letter to know that it will be an identifier or keyword
            elif self.current_char in LETTERS:
                token_list.append(self.make_identifier())

            # check it it's a digit and since numbers are more than one character create the number
            elif self.current_char in DIGITS:
                token_list.append(self.make_number())

            # check if it's an arithmetic
            elif self.current_char == '+':
                token_list.append(Token(TT_PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '-':
                token_list.append(Token(TT_MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == '*':
                token_list.append(Token(TT_MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == '/':
                token_list.append(Token(TT_DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == '^':
                token_list.append(Token(TT_POW, pos_start=self.pos))
                self.advance()

            # check if it's a pair
            elif self.current_char == '(':
                token_list.append(Token(TT_R_PAREN))
                self.advance()
            elif self.current_char == ')':
                token_list.append(Token(TT_L_PAREN))
                self.advance()

            # Comparators and logical operators
            elif self.current_char == '<':
                token_list.append(self.make_less_than())
            elif self.current_char == '>':
                token_list.append(self.make_greater_than())
            elif self.current_char == '=':
                token_list.append(self.make_equals())
            elif self.current_char == '!':
                full_token, mismatch_error = self.make_not_equals()
                if mismatch_error:
                    return [], mismatch_error

                token_list.append(full_token)

            # character was not recognized
            else:
                pos_start = self.pos.copy()

                char = self.current_char
                self.advance()

                # breaks the code and shows illegal character found
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        # returns the list of tokens found in order and no error
        return token_list, None

    #
    def make_number(self):
        num_str = ''
        dot_count = 0

        pos_start = self.pos.copy()

        # Check if next character is also a digit or a dot in order to create the number
        while self.current_char is not None and self.current_char in DIGITS + '.':

            # a '.' indicates that the number is a float
            if self.current_char == '.':
                # There can't be more than 1 dot in a float ie 233.1.5
                if dot_count == 1:
                    break

                dot_count += 1
                num_str += '.'

            # If it's not a dot then it is a digit
            else:
                num_str += self.current_char

            self.advance()

        # Assigns the Token Type if there is a dot= float or not = int
        if dot_count == 0:
            return Token(TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_identifier(self):
        identifier_string = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            identifier_string += self.current_char
            self.advance()

        token_type = TT_KEYWORD if identifier_string in KEYWORDS else TT_IDENTIFIER

        return Token(token_type, identifier_string, pos_start, self.pos)

    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()  # because we know that '!' called this method

        # Determine if '!='
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_equals(self):
        token_type = TT_EQUALS
        pos_start = self.pos.copy()
        self.advance()  # because we know that '=' called this method

        # Determine if '=' || '=='
        if self.current_char == '=':
            self.advance()
            token_type = TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        token_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()  # because we know that '<' called this method

        # Determine if '<' || '<='
        if self.current_char == '=':
            self.advance()
            token_type = TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        token_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()  # because we know that '>' called this method

        # Determine if '>' || '>='
        if self.current_char == '=':
            self.advance()
            token_type = TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

########################################################################################################################
#   RUN:
#
#   A test ground for how the lexer might be used
########################################################################################################################


if __name__ == '__main__':

    file_name = "Console"
    micro_c_code = "read int i = ( 2.13 + 5) i >= 3 write(i)"

    lexer = Lexer(file_name, micro_c_code)
    tokens, error = lexer.make_tokens()

    if error:
        print(error)
    else:
        print(tokens)
