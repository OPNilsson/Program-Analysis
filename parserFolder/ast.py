# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 14:56:17 2021

@author: stefa
"""

class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left, token, right):
        self.left = left
        self.right = right
        self.token = token

class Integer(object):
    def __init__(self, token, value):
        self.token = token
        self.value = token.value
        
