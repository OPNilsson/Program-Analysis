########################################################################################################################
#   Error:
#
#   This class is used when an error happens within the parser
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

