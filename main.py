########################################################################################################################
#   Main Program:
#
#   This file runs the program in the intended format
########################################################################################################################
from compiler.lexer import Lexer

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

    print(micro_c_code)

    lexer = Lexer(file_name, micro_c_code)
    tokens, error = lexer.make_tokens()

    if error:
        print(error)

