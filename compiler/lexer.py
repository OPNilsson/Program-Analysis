########################################################################################################################
#   Error:
#
#   This class is used when an error happens within the lexer
########################################################################################################################
import string
from compiler.static import *


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





class Token:
    def __init__(self, type, value=None, pos_start=None, pos_end=None):
        self.type = type
        self.value = value

        # if pos_start:
        #     self.pos_start = pos_start.copy()
        #     self.pos_end = pos_start.copy()
        #     self.pos_end.advance()

        # if pos_end:
        #     self.pos_end = pos_end

    # checks if the token matches the given type and value
    def matcher(self, type, value):
        return self.type == type and self.value == value

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

LETTERS = string.ascii_letters
DIGITS = '0123465789'

LETTERS_DIGITS = LETTERS + DIGITS


class Lexer:

    def __init__(self, micro_code_txt):
        self.text = micro_code_txt
        # print(self.text)
        # The current position and character that the lexer is looking at
        # pos starts at -1 because the lexer immediately advances a position when constructed
        # self.pos = Position(-1, 0, -1, self.fn)
        self.pos = 0
        self.current_char = self.text[self.pos]

        # self.advance()

    # Advances one position in the text and sets the current_char
    def advance(self):
        # is the same as self.pos += 1 but using custom position object to keep track of line and col
        # self.pos.advance(self.current_char)

        # # Sets the current character equal to that of the position unless it's the end of the text
        # self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

            
    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

            
    def make_number(self):
        # num_str = ''
        # dot_count = 0

        # pos_start = self.pos.copy()

        # # Check if next character is also a digit or a dot in order to create the number
        # while self.current_char is not None and self.current_char in DIGITS + '.':

        #     # a '.' indicates that the number is a float
        #     if self.current_char == '.':
        #         # There can't be more than 1 dot in a float ie 233.1.5
        #         if dot_count == 1:
        #             break

        #         dot_count += 1
        #         num_str += '.'

        #     # If it's not a dot then it is a digit
        #     else:
        #         num_str += self.current_char

        #     self.advance()

        # Assigns the Token Type if there is a dot= float or not = int
        # if dot_count == 0:
        #     return Token(TT_INT, int(num_str), pos_start, self.pos)
        # else:
        #     return Token(TT_FLOAT, float(num_str), pos_start, self.pos)
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)
        
        
    def get_next_token(self):
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(TT_INT, self.make_number())

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


    # Assigns the current char to a Token and appends it to the tokens list
    def make_tokens(self):
        token_list = []

        # While the currentChar is not the end of the text
        while self.current_char is not None:

            # ignore spaces, tabs, and new lines
            if self.current_char in ' \t\n':
                self.advance()

            # check if it's a letter to know that it will be an identifier or keyword
            elif self.current_char in LETTERS:
                token_list.append(self.make_identifier())

            # check it it's a digit and since numbers are more than one character create the number
            elif self.current_char in DIGITS:
                token_list.append(self.make_number())

            # end line ;
            elif self.current_char == ';':
                token_list.append(Token(TT_EL, pos_start=self.pos))
                self.advance()

            elif self.current_char == '.':
                token_list.append(Token(TT_METHOD, pos_start=self.pos))
                self.advance()

            # if " then make a string token
            elif self.current_char == '"':
                token_list.append(self.make_string())

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
                token_list.append(Token(TT_L_PAREN))
                self.advance()
            elif self.current_char == ')':
                token_list.append(Token(TT_R_PAREN))
                self.advance()
            elif self.current_char == '{':
                token_list.append(Token(TT_L_BRACKET))
                self.advance()
            elif self.current_char == '}':
                token_list.append(Token(TT_R_BRACKET))
                self.advance()
            elif self.current_char == '[':
                token_list.append(Token(TT_L_SQUARE))
                self.advance()
            elif self.current_char == ']':
                token_list.append(Token(TT_R_SQUARE))
                self.advance()

            # Comparators and logical operators
            elif self.current_char == '<':
                token_list.append(self.make_less_than())
            elif self.current_char == '>':
                token_list.append(self.make_greater_than())
            elif self.current_char == '=':
                token_list.append(self.make_equals())
            elif self.current_char == ':':
                full_token, mismatch_error = self.make_assign()
                if mismatch_error:
                    return [], mismatch_error
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

    # gather digits after the initial digit has been found in order to make a number of type INT or FLOAT
    

    # Makes an Identifier token and adds it to the array
    def make_identifier(self):
        identifier_string = ''
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in LETTERS_DIGITS + '_':
            identifier_string += self.current_char
            self.advance()

        token_type = TT_KEYWORD if identifier_string in KEYWORDS else TT_IDENTIFIER

        return Token(token_type, identifier_string, pos_start, self.pos)

    # Makes an assigner token := by checking that = comes after : or else throws mismatch error
    def make_assign(self):
        pos_start = self.pos.copy()
        self.advance()  # because we know that ':' called this method

        # Determine if ':='
        if self.current_char == '=':
            self.advance()
            return Token(TT_ASSIGN, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after ':')")

    # Makes a != token by checking what comes after the ! returns error if no =
    def make_not_equals(self):
        pos_start = self.pos.copy()
        self.advance()  # because we know that '!' called this method

        # Determine if '!='
        if self.current_char == '=':
            self.advance()
            return Token(TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    # Makes an equals token of types = | ==
    def make_equals(self):
        token_type = TT_EQUALS
        pos_start = self.pos.copy()
        self.advance()  # because we know that '=' called this method

        # Determine if '=' || '=='
        if self.current_char == '=':
            self.advance()
            token_type = TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    # makes a < token or a <=
    def make_less_than(self):
        token_type = TT_LT
        pos_start = self.pos.copy()
        self.advance()  # because we know that '<' called this method

        # Determine if '<' || '<='
        if self.current_char == '=':
            self.advance()
            token_type = TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    # makes a > or >=
    def make_greater_than(self):
        token_type = TT_GT
        pos_start = self.pos.copy()
        self.advance()  # because we know that '>' called this method

        # Determine if '>' || '>='
        if self.current_char == '=':
            self.advance()
            token_type = TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_string(self):
        string_var = ''
        escape_char = False  # Checks for string escape characters such as \ || \n

        pos_start = self.pos.copy()
        self.advance()  # because we know that '>' called this method

        # Dictionary of accepted escape characters such as \n or \t
        escape_characters = {
            'n': '\n',
            't': '\t'
        }

        # As long as it's not the end of the input or the end of the string builder " then it's part of the string_var
        while self.current_char is not None and (self.current_char != '"' or escape_char):
            # If the previous char in the string was \ then anything is accepted after
            if escape_char:
                # checks for character replacements in the dictionary
                string_var += escape_characters.get(self.current_char, self.current_char)
                escape_char = False
            else:
                # Checks for escape character \
                if self.current_char == '\\':
                    escape_char = True
                else:
                    string_var += self.current_char
                    escape_char = False

            self.advance()

        self.advance()  # because it stops on the "

        return Token(TT_STRING, string_var, pos_start, self.pos)


########################################################################################################################
#   RUN:
#
#   A test ground for how the lexer might be used
########################################################################################################################


# if __name__ == '__main__':

#     file_name = "Console"
#     micro_c_code = """
#     { int i;
#         {int fst; int snd} R;
#         int[10] A;
#         while (i < 10)
#             { read A[i];
#                 i := i + 1;
#             }
#         i := 0;
#         while (i < 10)
#             { if (A[i] >= 0)
#                 { R.fst := R.fst + A[i];
#                     i := i + 1;
#                 }
#             else { i := i + 1;
#                 break;
#             }
#             R.snd := R.snd + 1;
#             }
#         write (R.fst_R.snd);
#     }
#     """

#     print(micro_c_code)

#     lexer = Lexer(file_name, micro_c_code)
#     tokens, error = lexer.make_tokens()

#     if error:
#         print(error)
#     else:
#         print(tokens)
