from pyparsing import *
from worklist import *
from livevariable import *
from programgraph import *

ParserElement.enablePackrat()

LPAR, RPAR, LBRACK, RBRACK, LBRACE, RBRACE, SEMI, COMMA, DOT = map(Suppress, "()[]{};,.")
INT, CHAR, RECORD, ARRAY, FST, SND,  WHILE, IF, ELSE, RETURN, READ, WRITE = map(
    Keyword, "int char R A fst snd while if else return read write".split()
)


NAME = Word(alphas + "_", alphanums + "_")
NUM = Word(nums)
integer = Regex(r"[+-]?\d+")
char = Regex(r"'.'")
string_ = dblQuotedString


expr = Forward()
TYPE = Group((INT | CHAR))
func_call = Group(NAME + LPAR + Group(Optional(delimitedList(expr))) + RPAR)
array_acc = Group(ARRAY + LBRACK + (NAME | NUM) + RBRACK)
record_acc = Group(RECORD + DOT + (FST | SND))
operand = record_acc | array_acc | func_call | NAME | integer | char | string_


expr <<= infixNotation(
    operand,
    [
        (oneOf("- *"), 1, opAssoc.RIGHT),
        (oneOf("++ --"), 1, opAssoc.RIGHT),
        (oneOf("++ --"), 1, opAssoc.LEFT),
        (oneOf("/ %"), 2, opAssoc.LEFT),
        (oneOf("+ -"), 2, opAssoc.LEFT),
        (oneOf("< == > <= >= !="), 2, opAssoc.LEFT),
        (Regex(r"(?<!=):=(?!=)"), 2, opAssoc.LEFT),
    ],
) + Optional(
    LPAR + Group(Optional(delimitedList(expr))) + RPAR
)

stmt = Forward()
if_stmt = IF - LPAR + expr + RPAR + stmt + Optional(ELSE + stmt)
while_stmt = WHILE - LPAR + expr + RPAR + stmt
return_stmt = RETURN - expr + SEMI
read_stmt = READ + expr + SEMI
write_stmt = WRITE + expr + SEMI

stmt << Group(
    if_stmt
    | while_stmt
    | return_stmt
    | read_stmt
    | write_stmt
    | expr + SEMI
    | LBRACE + ZeroOrMore(stmt) + RBRACE
    | SEMI
)

var_decl = Group(TYPE + NAME + Optional(LBRACK + integer + RBRACK)) + SEMI
rec_body = TYPE + FST + SEMI + TYPE + SND

rec_decl = Group(
    LBRACE
    + Group(rec_body)
    + RBRACE
    + RECORD
) + SEMI

array_decl = Group(
    TYPE
    + LBRACK
    + NUM
    + RBRACK
    + ARRAY
) + SEMI

arg = Group(TYPE + NAME)
fun_body = ZeroOrMore(var_decl) + ZeroOrMore(rec_decl) + ZeroOrMore(array_decl) + ZeroOrMore(stmt)
fun_decl = Group(
    TYPE
    + NAME
    + LPAR
    + Optional(Group(delimitedList(arg)))
    + RPAR
    + LBRACE
    + Group(fun_body)
    + RBRACE
)


decl = fun_decl | var_decl | rec_decl | array_decl
program = ZeroOrMore(decl) + ZeroOrMore(stmt)

program.ignore(cStyleComment)

# set parser element names
for vname in (
        "if_stmt while_stmt return_stmt read_stmt write_stmt TYPE "
        "NAME fun_decl var_decl rec_decl array_decl program arg fun_body stmt".split()
):
    v = vars()[vname]
    v.setName(vname)

def main():
    average = r"""
    /* Just a comment! */
    int main() {
        int i;
        {int fst; int snd} R;
        int[10] A;
        i := A[1];
        while(i < 10) {
            i++;
            read A[i];
        }
        if (i > 10) {
            i := R.fst;
        } else {
            i := R.snd;
        }
        write R.fst/R.snd;
        return 0;
    }    
    """

    fib = r"""
    z := 1; 
    y := 0;
    t := 0;
    for (i := 0; i < x; i := i + 1;){
        t := z;
        z := y;
        y := t + z;
    }
    """

    nested = r"""
    x := 0; 
    y := 0;
    z := 0;
    while(x < 10){
        x := x + 1;
        
        while (y < 10){
            y := y + 1;
            
            while(z < 10){
                z := z + 1;
            }
        }
    }
    """

    choice = input()

    if choice == "1":
        ast = program.parseString(average, parseAll=True)
    elif choice == "2":
        ast = program.parseString(fib, parseAll=True)
    else:
        ast = program.parseString(nested, parseAll=True)

    ast.pprint()

    w = list()
    fifo = FIFO()

    print()
    print(ast.dump())

    print("-----------------------------------------")

    PG_Builder = ProgramGraph(ast)
    pg = PG_Builder.getPG()

    print("-----------------------------------------")
    for node in pg:
        print(node.value)
        w = fifo.insert(node, w)

    lv = LiveVariable(w)

    iteration = 0
    for node in w:
        iteration += 1
        lv.solve(node)
        iteration += lv.i

    print(iteration)

if __name__ == "__main__":
    main()
