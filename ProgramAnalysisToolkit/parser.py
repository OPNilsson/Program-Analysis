from lark import Lark

assignment_grammar = """ 
statements: NEWLINE* (assignment (NEWLINE | ";"))* expression NEWLINE* 
assignment: CNAME ":=" expression 
         | CNAME ":=" "{" statements "}" 
%import common.WS_INLINE 
%import common.NEWLINE 
%ignore WS_INLINE 
"""


expression_grammar = """ 
arith:   term   | term "+" arith  -> add | term "-" arith      -> sub 
term:    factor | factor "*" term -> mul | factor "/" term     -> div 
factor:  pow    | "+" factor      -> pos | "-" factor          -> neg 
pow:     call ["**" factor] 
call:    atom   | call trailer 
atom:    "(" expression ")" | CNAME -> symbol | NUMBER -> literal 
trailer: "(" arglist ")" 
arglist: expression ("," expression)* 
%import common.CNAME 
%import common.NUMBER 
%import common.WS 
"""


branching_grammar = """
block:      expression | "{" statements "}"
branch:     "if" expression "{" block "}" "else" "{" block "}"
iteration: "while" "(" expression ")" "{" block "}"
 
or:         and        | and "or" and
and:        not        | not "and" not
not:        comparison | "not" not -> not_test
comparison: arith | arith "==" arith -> eq | arith "!=" arith -> ne
                  | arith ">" arith -> gt  | arith ">=" arith -> ge
                  | arith "<" arith -> lt  | arith "<=" arith -> le
"""


class AST:
    _fields = ()

    def __init__(self, *args, line=None):
        self.line = line
        for n, x in zip(self._fields, args):
            setattr(self, n, x)
            if self.line is None: self.line = x.line


class Literal(AST):
    _fields = ("value",)
    def __str__(self): return str(self.value)


class Symbol(AST):
    _fields = ("symbol",)

    def __str__(self): return self.symbol


class Call(AST):                                 # Call: evaluate a function on arguments
    _fields = ("function", "arguments")

    def __str__(self):
        return "{0}({1})".format(str(self.function), ", ".join(str(x) for x in self.arguments))


class Block(AST):
    _fields = ("statements",)

    def __str__(self):
        return "{" + "; ".join(str(x) for x in self.statements) + "}"


class Assign(AST):
    _fields = ("symbol", "value")

    def __str__(self):
        return "{0} := {1}".format(str(self.symbol), str(self.value))


class SymbolTable:
    def __init__(self, parent=None, **symbols):
        self.parent = parent
        self.symbols = symbols

    def __getitem__(self, symbol):
        if symbol in self.symbols:
            return self.symbols[symbol]
        elif self.parent is not None:
            return self.parent[symbol]
        else:
            raise KeyError(symbol)

    def __setitem__(self, symbol, value):
        self.symbols[symbol] = value



grammar = "\n".join(["start: statements", "expression: or | branch"]
                   ) + expression_grammar + assignment_grammar + branching_grammar


parser = Lark(grammar)


class UserError(Exception):
    pass


def run(astnode, symbols):
    if isinstance(astnode, Call) and astnode.function.symbol == "if":
        predicate  = run(astnode.arguments[0], symbols)
        consequent = run(astnode.arguments[1], symbols)
        alternate  = run(astnode.arguments[2], symbols)
        return consequent if predicate else alternate

    elif isinstance(astnode, Literal):
        return astnode.value
    elif isinstance(astnode, Symbol):
        return symbols[astnode.symbol]
    elif isinstance(astnode, Call):
        function = run(astnode.function, symbols)
        arguments = [run(x, symbols) for x in astnode.arguments]
        return function(*arguments)
    elif isinstance(astnode, Block):
        symboltable = SymbolTable(symbols)
        for statement in astnode.statements:
            last = run(statement, symboltable)
        return last
    elif isinstance(astnode, Assign):
        symbols[astnode.symbol] = run(astnode.value, symbols)


def showline(ast):
    if isinstance(ast, list):
        for x in ast:
            showline(x)
    if isinstance(ast, AST):
        print("{0:5s} {1:10s} {2}".format(str(ast.line), type(ast).__name__, ast))
        for n in ast._fields:
            showline(getattr(ast, n))


import math, operator
symbols = {**operator.__dict__, **math.__dict__}
builtins = SymbolTable(**{**operator.__dict__, **math.__dict__})


def toast(ptnode):
    if ptnode.data == "branch":
        predicate, consequent, alternate = [toast(x) for x in ptnode.children]
        return Call(Symbol("if", line=predicate.line), [predicate, consequent, alternate])

    if ptnode.data == 'iteration':
        condition, block = [toast(x) for x in ptnode.children]
        return Call(Symbol("if", line=condition.line), [condition, block])

    elif ptnode.data in ("or", "and", "eq", "ne", "gt", "ge", "lt", "le") and len(ptnode.children) > 1:
        arguments = [toast(x) for x in ptnode.children]
        return Call(Symbol(str(ptnode.data), line=arguments[0].line), arguments)

    elif ptnode.data == "not_test":
        argument = toast(ptnode.children[0])
        return Call(Symbol("not", line=argument.line), [argument])

    elif ptnode.data == "statements":
        statements = [toast(x) for x in ptnode.children if x != "\n"]
        if len(statements) == 1:
            return statements[0]
        else:
            return Block(statements, line=statements[0].line)
    elif ptnode.data == "assignment":
        return Assign(str(ptnode.children[0]), toast(ptnode.children[1]), line=ptnode.children[0].line)
    elif ptnode.data in ("add", "sub", "mul", "div", "pos", "neg"):
        arguments = [toast(x) for x in ptnode.children]
        return Call(Symbol(str(ptnode.data), line=arguments[0].line), arguments)
    elif ptnode.data == "pow" and len(ptnode.children) == 2:
        arguments = [toast(ptnode.children[0]), toast(ptnode.children[1])]
        return Call(Symbol("pow", line=arguments[0].line), arguments)
    elif ptnode.data == "call" and len(ptnode.children) == 2:
        return Call(toast(ptnode.children[0]), toast(ptnode.children[1]))
    elif ptnode.data == "symbol":
        return Symbol(str(ptnode.children[0]), line=ptnode.children[0].line)
    elif ptnode.data == "literal":
        return Literal(float(ptnode.children[0]), line=ptnode.children[0].line)
    elif ptnode.data == "arglist":
        return [toast(x) for x in ptnode.children]
    else:
        return toast(ptnode.children[0])


builtins["if"] = lambda predicate, consequent, alternate: consequent if predicate else alternate
builtins["or"] = lambda p, q: p or q
builtins["and"] = lambda p, q: p and q
builtins["not"] = lambda p: not p


def show(x, y, f):
    print(f, x, y, f(x, y))
    return f(x, y)


def make_while(condition, f):
    while condition:
        f()

builtins["add"] = lambda x, y: show(x, y, operator.add)
builtins["mul"] = lambda x, y: show(x, y, operator.mul)
builtins["gt"] = lambda x, y: show(x, y, operator.gt)
builtins["lt"] = lambda x, y: show(x, y, operator.lt)

symboltable = SymbolTable(**{**operator.__dict__, **math.__dict__})

symboltable["if"] = (lambda predicate, consequent, alternate:
                         consequent() if predicate else alternate())

symboltable["add"] = lambda x, y: show(x, y, operator.add)
symboltable["mul"] = lambda x, y: show(x, y, operator.mul)
symboltable["while"] = lambda condition, f: make_while(condition, f)


print(run(toast(parser.parse("x := 1; if x == x { 2 + 2 } else { 111 * 9 }")), SymbolTable(symboltable)))

