# TITLE: Study and perform YAcc and Lex.
# AIM: Write a program to implement to YAcc and Lex in Java
# Theory:
# 1. YAcc
# Yacc (Yet Another Compiler Compiler) is a tool that generates a parser from a grammar specification file.
# It is typically used in conjunction with Lex, a lexical analyzer that generates tokens from input text.
# Yacc reads a file containing a context-free grammar specification and generates a parser that can recognize
# input conforming to that grammar. The grammar specification file typically includes rules that define how
# different elements of the input are parsed and combined into larger structures.
# To use Yacc, you must define the grammar rules for the language you want to parse using BNF notation.
# Yacc generates a parser in C, which can then be compiled and used to parse input text.
# The Yacc parser uses a stack-based algorithm to parse the input text. As input text is read, the parser builds
# a parse tree, which represents the structure of the input text according to the grammar rules.
# Yacc is often used in the development of programming language compilers and interpreters, as well as in
# other applications that require parsing complex input.
# 2. Lex
# Lex is a tool that generates lexical analyzers, or lexers, which recognize and categorize sequences of
# characters in input text. Lex operates by generating a finite-state machine that recognizes regular
# expressions.
# To use Lex, you must define a set of regular expressions and the corresponding actions to be taken when
# those expressions are matched in the input text. The regular expressions are typically defined using a
# syntax similar to that of regular expressions in other contexts.
# Lex generates a C program that implements the lexer, which can then be compiled and used to process
# input text. The generated lexer reads input text one character at a time and matches it against the defined
# regular expressions.


#code
import re

# ---------------- Constant Folding ----------------
def constant_folding(statement):
    try:
        left, right = statement.split("=")
        right = right.strip()
        if re.match(r'^\d+\s*[\+\-\*/]\s*\d+$', right):
            result = eval(right)
            return f"{left.strip()} = {result}"
    except:
        pass
    return statement

# ---------------- Constant Propagation ----------------
def constant_propagation(statements):
    constants = {}
    optimized = []
    for stmt in statements:
        left, right = stmt.split("=")
        left = left.strip()
        right = right.strip()

        # replace known constants
        for var in constants:
            right = right.replace(var, str(constants[var]))

        # store constant
        if right.isdigit():
            constants[left] = int(right)

        optimized.append(f"{left} = {right}")
    return optimized

# ---------------- Dead Code Elimination ----------------
def dead_code_elimination(statements):
    used = set()
    optimized = []

    for stmt in reversed(statements):
        left, right = stmt.split("=")
        left = left.strip()
        right = right.strip()

        if left in used or stmt == statements[-1]:
            optimized.append(stmt)
            vars_used = re.findall(r'[a-zA-Z]+', right)
            used.update(vars_used)

    optimized.reverse()
    return optimized

# ---------------- Main Optimization ----------------
def optimize_code(statements):
    print("\nAfter Constant Folding:")
    folded = [constant_folding(s) for s in statements]
    for i in folded:
        print(i)

    print("\nAfter Constant Propagation:")
    propagated = constant_propagation(folded)
    for i in propagated:
        print(i)

    print("\nAfter Dead Code Elimination:")
    final = dead_code_elimination(propagated)
    for i in final:
        print(i)

# ---------------- Input ----------------
n = int(input("Enter number of statements: "))
statements = []

print("Enter statements (example: a = 5 + 3):")
for i in range(n):
    statements.append(input())

print("\nOriginal Code:")
for s in statements:
    print(s)

optimize_code(statements)

# input & output
# Enter number of statements: 4
# Enter statements (example: a = 5 + 3):
# a=6+7
# b=a+2
# c=b+c
# d=7*d

# Original Code:
# a=6+7
# b=a+2
# c=b+c
# d=7*d

# After Constant Folding:
# a = 13
# b=a+2
# c=b+c
# d=7*d

# After Constant Propagation:
# a = 13
# b = 13+2
# c = b+c
# d = 7*d

# After Dead Code Elimination:
# d = 7*d
