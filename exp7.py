# Experiment No. 7
# TITLE: Implementation of code generation phase of compiler.
# AIM: Write a program to implement code generation for the given grammar in Python /Java
# Theory:
# What is Code Generation?
# The first part of a compiler analyzes the source code into a structure that carries the meaning of the program; this
# structure is generally the abstract syntax tree that’s been checked and decorated. (Remember decorated means all
# identifier references have been resolved.)
# From this structure we can generate the corresponding code in some other language, the target language. This is
# what a code generator does.
# Register and Address Descriptors:
# A register descriptor contains the track of what is currently in each register. The register descriptors show that all
# the registers are initially empty.
# An address descriptor is used to store the location where current value of the name can be found at run time.

##### A code-generation algorithm: #####

# The algorithm takes a sequence of three-address statements as input. For each three address statement of the form
# a:= b op c perform the various actions. These are as follows:
# 1. Invoke a function getreg to find out the location L where the result of computation b op c should be stored.
# 2. Consult the address description for y to determine y&#39;. If the value of y currently in memory and register
# both then prefer the register y&#39; . If the value of y is not already in L then generate the instruction MOV y&#39;
# , L to place a copy of y in L.
# 3. Generate the instruction OP z&#39; , L where z&#39; is used to show the current location of z. if z is in both then
# prefer a register to a memory location. Update the address descriptor of x to indicate that x is in location
# L. If x is in L then update its descriptor and remove x from all other descriptor.
# 4. If the current value of y or z have no next uses or not live on exit from the block or in register then alter
# the register descriptor to indicate that after execution of x : = y op z those register will no longer contain
# y or z.


#code
# Implementation of Code Generation Phase

def generate_code(statements):
    for stmt in statements:
        # remove spaces
        stmt = stmt.replace(" ", "")

        # split LHS and RHS
        if '=' not in stmt:
            print(f"Invalid statement: {stmt}")
            continue

        lhs, rhs = stmt.split('=')

        op = None
        left = right = None

        # find operator
        for operator in ['+', '-', '*', '/']:
            if operator in rhs:
                op = operator
                left, right = rhs.split(operator)
                break

        # if no operator (simple assignment)
        if op is None:
            print(f"MOV R0, {rhs}")
            print(f"MOV {lhs}, R0\n")
            continue

        # generate code
        print(f"MOV R0, {left}")

        if op == '+':
            print(f"ADD R0, {right}")
        elif op == '-':
            print(f"SUB R0, {right}")
        elif op == '*':
            print(f"MUL R0, {right}")
        elif op == '/':
            print(f"DIV R0, {right}")

        print(f"MOV {lhs}, R0\n")


# ---------------- MAIN ----------------
def main():
    try:
        n = int(input("Enter the number of statements: "))
    except ValueError:
        print("Invalid number!")
        return

    print("Enter the statements:")
    statements = []

    for _ in range(n):
        statements.append(input())

    print("\nGenerated Code:\n")
    generate_code(statements)


if __name__ == "__main__":
    main()

# input & output
# Enter the number of statements: 5
# Enter the statements:
# t1=a+b
# t2=c-d
# t3=t1+t2
# t4=t3/e
# result=t4+f

# Generated Code:

# MOV R0, a
# ADD R0, b
# MOV t1, R0

# MOV R0, c
# SUB R0, d
# MOV t2, R0

# MOV R0, t1
# ADD R0, t2
# MOV t3, R0

# MOV R0, t3
# DIV R0, e
# MOV t4, R0

# MOV R0, t4
# ADD R0, f
# MOV result, R0
