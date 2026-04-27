# Implementation of Top Down Parser
# AIM: Write a Program to implement Recursive Decent Parser in Python/Java.
# Theory:
# A parse tree is an entity which represents the structure of the derivation of a terminal string
# from some non-terminal (not necessarily the start symbol).
# The definition is as in the book. Key features to define are the root ∈ V and yield ∈ Σ* of
# each tree.
# For each σ ∈ Σ, there is a tree with root σ and no children; its yield is σ
# For each rule A → ε, there is a tree with root A and one child ε; its yield is ε If
# t1, t2, ..., tn are parse trees with roots r1, r2, ..., rn and respective
# yields y1, y2, ..., yn, and A → r1r2...rn is a production, then there is a parse tree with
# root A whose children are t1, t2, ..., tn. Its root is A and its yield is y1y2...yn
# Observe that parse trees are constructed from bottom up, not top down. The actual
# construction of &quot;adding children&quot; should be made more precise, but we intuitively know
# what&#39;s going on.
# The way the production rules are implemented (derivation) divides parsing into two types :
# top-down parsing and bottom-up parsing.

#code
SUCCESS = True
FAILED = False

cursor = 0
string = ""


def remaining():
    return string[cursor:] if cursor < len(string) else ""


def E():
    print(f"{remaining():16} E -> T E'")
    if T():
        return Edash()
    return FAILED


def Edash():
    global cursor

    if cursor < len(string) and string[cursor] == '+':
        print(f"{remaining():16} E' -> + T E'")
        cursor += 1
        if T():
            return Edash()
        return FAILED
    else:
        print(f"{remaining():16} E' -> ε")
        return SUCCESS


def T():
    print(f"{remaining():16} T -> F T'")
    if F():
        return Tdash()
    return FAILED


def Tdash():
    global cursor

    if cursor < len(string) and string[cursor] == '*':
        print(f"{remaining():16} T' -> * F T'")
        cursor += 1
        if F():
            return Tdash()
        return FAILED
    else:
        print(f"{remaining():16} T' -> ε")
        return SUCCESS


def F():
    global cursor

    if cursor < len(string) and string[cursor] == '(':
        print(f"{remaining():16} F -> ( E )")
        cursor += 1

        if E():
            if cursor < len(string) and string[cursor] == ')':
                cursor += 1
                return SUCCESS
        return FAILED

    elif cursor < len(string) and string[cursor].isalpha():
        # ✅ Accept any identifier like a, b, aa, eb
        print(f"{remaining():16} F -> id")
        while cursor < len(string) and string[cursor].isalpha():
            cursor += 1
        return SUCCESS

    return FAILED


# ===== MAIN =====
string = input("Enter the string: ").replace(" ", "")  # remove spaces
cursor = 0

print("\nInput\t\tAction")
print("--------------------------------")

if E() and cursor == len(string):
    print("--------------------------------")
    print("✅ String is successfully parsed")
else:
    print("--------------------------------")
    print("❌ Error in parsing")

# to run a program
# python filename.py

  
#input & output
# Enter the string: i+i*i

# Input		Action
# --------------------------------
# i+i*i            E -> T E'
# i+i*i            T -> F T'
# i+i*i            F -> id
# +i*i             T' -> ε
# +i*i             E' -> + T E'
# i*i              T -> F T'
# i*i              F -> id
# *i               T' -> * F T'
# i                F -> id
#                  T' -> ε
#                  E' -> ε
# --------------------------------
# ✅ String is successfully parsed
