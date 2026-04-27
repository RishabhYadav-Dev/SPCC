# TITLE: To Study Design and implementation of Lexical Analyser.
# AIM: Write a program to implement lexical Analyzer(Tokenization) in Java/Python
# Theory:
# Lexical analysis is the first phase of a compiler. It takes the modified source code from language
# preprocessors that are written in the form of sentences. The lexical analyzer breaks these
# syntaxes into a series of tokens, by removing any whitespace or comments in the source code.
# If the lexical analyzer finds a token invalid, it generates an error. The lexical analyzer works
# closely with the syntax analyzer. It reads character streams from the source code, checks for
# legal tokens, and passes the data to the syntax analyzer when it demands.

  #code ##
import re

# Define token constants
ID = "Identifier"
NUM = "Number"
OPERATOR = "Operator"
PAREN = "Parenthesis"
ASSIGN = "Assignment Operator"
REL_OP = "Relational Operator"
KEYWORD = "Keyword"
DONE = "Done"

# Define keywords
keywords = {
    "if": KEYWORD, "else": KEYWORD, "for": KEYWORD,
    "int": KEYWORD, "float": KEYWORD, "double": KEYWORD,
    "char": KEYWORD, "struct": KEYWORD, "return": KEYWORD
}

# Function to analyze tokens
def lexer(input_str):
    tokens = []
    lines = input_str.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        pattern = r'[a-zA-Z_]\w*|\d+|==|!=|<=|>=|\+|-|\*|/|\(|\)|=|<|>'
        words = re.findall(pattern, line)

        for word in words:
            if word.isdigit():
                tokens.append((NUM, word))
            elif word in keywords:
                tokens.append((KEYWORD, word))
            elif word in ('(', ')'):
                tokens.append((PAREN, word))
            elif word == '=':
                tokens.append((ASSIGN, word))
            elif word in ('<', '>', '<=', '>=', '==', '!='):
                tokens.append((REL_OP, word))
            elif word in ('+', '-', '*', '/'):
                tokens.append((OPERATOR, word))
            else:
                tokens.append((ID, word))

    tokens.append((DONE, None))
    return tokens

# Main program
def main():
    print("\t\tProgram For Lexical Analysis.")
    print("Enter the Input:")

    input_str = ""
    while True:
        line = input()
        if line.strip() == "" and input_str.strip() != "":
            break
        input_str += line + "\n"

    tokens = lexer(input_str)

    print("\nOutput:")
    for token in tokens:
        if token[0] == DONE:
            print("Done")
        else:
            print(f"{token[0]}: {token[1]}")

# ✅ Correct entry point
if __name__ == "__main__":
    main()

  # To Run Program
  # python filename.py


# # input
# 		Program For Lexical Analysis.
# Enter the Input:-
# int a = 10;
# if a > 5
# int b = a;
# int temp = 0;


# Output:
# Keyword: int
# Identifier: a
# Assignment Operator: =
# Number: 10
# Keyword: if
# Identifier: a
# Relational Operator: >
# Number: 5
# Keyword: int
# Identifier: b
# Assignment Operator: =
# Identifier: a
# Keyword: int
# Identifier: temp
# Assignment Operator: =
# Number: 0
# Done
