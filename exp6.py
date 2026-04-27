# TITLE: Design and Implement Intermediate Code generation
# AIM: Write a program to implement Three address code generation in Python/Java
# Theory:
# Code generation is one of the least formalized subjects in compiler construction. The task of the code generation
# phase of a compiler is, to take as input a given internal form representation of the source program &amp; to produce
# as output an equivalent sequence of instructions in the language of the object machine. Purpose of this phase is
# to produce the appropriate code either in assembly or machine language. This phase has parse tree as input, it uses
# code productions or rules. These productions define the operators we encounter in the parse trees. This phase tries
# to transform intermediate code into a form from which more efficient target code can be produced. Source
# Program Front end Analysis activities IC Code Optimization IC Code generator Target program Symbol table
# Literal table &amp; Other tables
# Intermediate code can translate the source program into the machine program. Intermediate code is generated
# because the compiler can’t generate machine code directly in one pass. Therefore, first, it converts the source
# program into intermediate code, which performs efficient generation of machine code further. The intermediate
# code can be represented in the form of postfix notation, syntax tree, directed acyclic graph, three address codes,
# Quadruples, and triples.


#code
tmpch = ord('Z')  # temporary variable names start from Z

class Exp:
    def __init__(self, pos, op):
        self.pos = pos
        self.op = op

str_exp = ""


# ---------------- Find Next Operator ----------------
def findopr():
    global str_exp

    # correct precedence
    ops = [
        ['*', '/'],
        ['+', '-']
    ]

    for level in ops:
        for i, ch in enumerate(str_exp):
            if ch in level:
                return Exp(i, ch)

    return None


# ---------------- Find Left ----------------
def fleft(x):
    global str_exp
    x -= 1

    while x >= 0:
        if str_exp[x] not in ['+', '*', '=', '-', '/', ':'] and str_exp[x] != '$':
            ch = str_exp[x]
            str_exp = str_exp[:x] + '$' + str_exp[x+1:]
            return ch
        x -= 1
    return ""


# ---------------- Find Right ----------------
def fright(x):
    global str_exp
    x += 1

    while x < len(str_exp):
        if str_exp[x] not in ['+', '*', '=', '-', '/', ':'] and str_exp[x] != '$':
            ch = str_exp[x]
            str_exp = str_exp[:x] + '$' + str_exp[x+1:]
            return ch
        x += 1
    return ""


# ---------------- Generate Code ----------------
def explore():
    global str_exp, tmpch

    print("\nThe intermediate code:\t\tExpression")

    while True:
        exp = findopr()
        if not exp:
            break

        left = fleft(exp.pos)
        right = fright(exp.pos)

        temp = chr(tmpch)
        tmpch -= 1

        # replace operator with temp
        str_exp = str_exp[:exp.pos] + temp + str_exp[exp.pos+1:]

        print(f"\t{temp} := {left} {exp.op} {right}\t\t", end="")

        for ch in str_exp:
            if ch != '$':
                print(ch, end="")
        print()


# ---------------- MAIN ----------------
def main():
    global str_exp

    print("\n\tINTERMEDIATE CODE GENERATION\n")
    str_exp = input("Enter the Expression : ").replace(" ", "")

    explore()


if __name__ == "__main__":
    main()


# input & output

# 	INTERMEDIATE CODE GENERATION

# Enter the Expression : e/a/m*p+l-e

# The intermediate code:		Expression
# 	Z := e / a		Z/m*p+l-e
# 	Y := Z / m		Y*p+l-e
# 	X := Y * p		X+l-e
# 	W := X + l		W-e
# 	V := W - e		V
