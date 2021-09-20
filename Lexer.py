#!/usr/bin/env python
"""Lexer.py: Parses Micro C language with the goal of creating http://www.formalmethods.dk/pa4fun/"""
from stack import Stack
import re
class Parser:
    # Checks two characters and returns whether they are a pair or not
    def __init__(self,microc):
        self.microc = microc
        self.rules = {}

        assignment = {
            'variable_assignment' : ':=',
            'array_assignment' : '.[.]=.'
        }
        arithmetic = {
            'abs' : '|x|',
            'plus' : '+',
            'minus':'-',
            'division' : '/',
            'multiplication':'*'
        }
        self.loops = {
            'for_loop':'for(){}',
            'while_loop':'while(){}'
        }
        comparrison = {
            'if':'if()',
            'equals':'=',
            'leq':'>',
            'req':'<'
        }

    def find_loops(self):
        i = 'for'
        re.match('for')
        y = re.findall(r'(?=' + re.escape(i) + r').*?(?<=})',self.microc)
        return y

    def find_assignments(self):
        x = re.findall('. := .',self.microc)
        return x








