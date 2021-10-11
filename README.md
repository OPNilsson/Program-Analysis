# Program-Analysis
A program which inputs Micro-C code and analyzes it. This is done through the use of a lexer, a parser, and a visualizer.
The three components interpret the code inputted and show if it follows Micro-C language rules.

The goal of the project was  creating a Micro-C equivalent of: http://www.formalmethods.dk/pa4fun/

## The Compiler
In oder to create analyzes of Micro-C code the program must first understand what that code is saying, and then present it to the user.
This process is broken down into three components: the identification of tokens, the formatting of the execution order, and the visualization for the user. 

### The Lexer
The Lexer is the simplest of the three main components of the compiler.
The lexer's function is to take in a file name and a string source of code. 
The lexer will then iterate through the code character by character until there is no more code or an error has occurred.
As the lexer iterates through the characters it will try to identify what these characters mean in accordance to Micro-C.
For example, take the following line of Micro-C code:

```Micro-C
{ int a; read(a); a = a + 2; write(a); }
```
The Lexer will start iterating through it and first encountering an i in the int identifier.
The Lexer will check if the character 'i' is a recognized character within the language dictionary. 
Since 'i' doesn't inherently mean anything to Micro-C an Illegal Error would usually be thrown at this point. 
However, the Lexer must recognize that 'i' is in int which is a recognized command in Micro-C. 
To do this, the Lexer keeps a dictionary of "Keywords" that it needs to keep an eye out for. 
So if a character is the start of a Keyword it will check if the following characters match the spelling of that keyword.

Some characters are not a keywords but simply require checking the next character to correctly identify them.
For example, the characters `` <= := == ``. 
In cases like these the Lexer is on the look-out for the first character and matches if the next one is what was expected.
If it wasn't then an Expected Character error is shown to the user.
Other characters such as ``= + - { ) `` are simply recognized immediately.

The following code shows the Lexer Constructor which simply takes the filename and the Micro-C code.
The constructor also shows a glimpse of how the lexer shows how the lexer operates. 
Storing a position with where in the code the lexer is, and using the advance method to iterate through the code identifiying what these characters mean.
Once the lexer identifies what the character(s) is/are they are categorized into what is known as a Token. 

The lexer will then return a list of Tokens that have been identified in the code as well as an error if one exists.

Lexer Constructor:
```python
class Lexer:

    def __init__(self, filename, micro_code_txt):
        self.text = micro_code_txt
        self.fn = filename

        self.pos = Position(-1, 0, -1, self.fn)
        self.current_char = None

        self.advance()
```

### The Parser

