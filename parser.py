#!/usr/bin/env python
"""parser.py: Parses Micro C language with the goal of creating http://www.formalmethods.dk/pa4fun/"""
from stack import Stack


# Checks two characters and returns whether they are a pair or not
def __has_matching_pair(character1, character2):
    if character1 == '(' and character2 == ')':
        return True
    elif character1 == '{' and character2 == '}':
        return True
    elif character1 == '[' and character2 == ']':
        return True
    else:
        return False


def __syntax_check(char_arr):

    rules = {
        "parentheses_open": ["(", "{", "["],
        "parentheses_close": [")", "}", "]"],
        "operators_arithmetic": ["+", "-", "*", "/", "%", "++", "--"],
        "operators_relation": ["<", ">", "<=", ">=", "==", "!="],
        "operators_logical": ["&&", "||", "!"]
    }

    # A stack is used to check for ordered pairs
    # ex) { () } ✓  { ( } )  ✗
    stack = Stack()

    i = 0
    while i < len(char_arr):

        # An ending comment has been found
        if char_arr[i] == '/' and char_arr[i + 1] == '*':
            index = i
            while index < len(char_arr):
                if char_arr[index] == '*' and char_arr[index + 1] == '/':
                    i = index
                    index = len(char_arr)
                index += 1

        # If there is 2 '/' in a row then the line is a comment and doesn't need to be checked for syntax
        if char_arr[i] == '/' and char_arr[i + 1] == '/':
            return True

        # If the arr[i] is a starting parenthesis then push it
        if char_arr[i] == '{' or char_arr[i] == '(' or char_arr[i] == '[':
            stack.push(char_arr[i])

        # If arr[i] is an ending parenthesis then pop from stack
        # check if the popped parenthesis is a matching pair
        if char_arr[i] == '}' or char_arr[i] == ')' or char_arr[i] == ']':
            # If we see an ending parenthesis without a pair then return false
            if stack.isEmpty():
                return False

            # Pop the top element from stack, if it is not a pair parenthesis of character then there is a mismatch.
            elif not __has_matching_pair(stack.pop(), char_arr[i]):
                return False
        i += 1

    # If the stack is empty then there is a lose parentheses or comment starter
    return stack.isEmpty()


if __name__ == '__main__':
    print("-------- Welcome to Micro C Parser --------")
    code_str_arr = input("Enter a at least one line of code: ").replace(" ", "")

    line_number = 0
    colon_count = 0

    # Counts ';' in code used for reference
    for char in code_str_arr:
        if ";" in char:
            colon_count += 1

    # Split the code into lines if more than one line
    line_str_arr = code_str_arr.split(";")

    # Loop through each line checking for syntax
    # TODO: Keep track of all the errors not just break at error
    for char_str_arr in line_str_arr:

        # Don't check empty lines
        if len(char_str_arr) != 0:

            line_number += 1

            print(line_number, "| ", char_str_arr)

            # Last line is missing a ';'
            if line_number <= colon_count:
               compiles =  __syntax_check(char_str_arr)

               if not compiles:
                   print('Line ', line_number, " Error!")

            else:
                print('Expected ";" at line ', line_number)
                break


