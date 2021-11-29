from compiler.interpreter import Interpreter
from compiler.lexer import Lexer
from compiler.parser import Parser

########################################################################################################################
#   Main Program:
#
#   This file runs the program in the intended format
########################################################################################################################
if __name__ == '__main__':

    file_name = "Console"
    micro_c_code = """
    { int i;
        {int fst; int snd} R;
        int[10] A;
        while (i < 10)
            { read A[i];
                i := i + 1;
            }
        i := 0;
        while (i < 10)
            { if (A[i] >= 0)
                { R.fst := R.fst + A[i];
                    i := i + 1;
                }
            else { i := i + 1;
                break;
            }
            R.snd := R.snd + 1;
            }
        write (R.fst_R.snd);
    }
    """

    test_code = """
            3 + 3
    """

    print(test_code)

    # Generates teh tokens and returns either the list of tokens or an error
    lexer = Lexer(file_name ,test_code)
    tokens, error = lexer.make_tokens()

    if error:
        print(error)
    else:
        print("Lexer Tokens:")
        print(tokens)

        # Generates the syntax tree and returns either the tree or the error
        parser = Parser(tokens)
        ast = parser.parse()

        if error:
            print(ast.error)
        else:
            print()
            print("Parser Priorities `()`")
            print(ast.node)

            interpreter = Interpreter()

            # Re configures the AST into a list of Node Objects
            interpreter.visit(ast.node)

            interpreter.view_tree()


