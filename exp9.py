# Title: Study and perform ACC and Lex
# Aim:To write a program to implement 1/ACC and LEX conccept using python


### Steps to perform or execute 9 exp ###
# step1:-first create three file name lexer.py parser.py calculator.py
# step2:- copy and paste code for seperate three files
# step3:-then execute only calculator.py by using this command in terminal python calculator.py

# ##lexer.py## #
import ply.lex as lex

tokens = (
    'NUMBER',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
)

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Invalid character: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

# ##parser.py## #
import ply.yacc as yacc
from lexer import tokens

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    if p[3] == 0:
        raise ZeroDivisionError("division by zero")
    p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_number(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

# ##calculator.py## #
from lexer import lexer
from parser import parser

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break

    if not s.strip():
        continue

    try:
        result = parser.parse(s, lexer=lexer)
        print(result)
    except Exception as e:
        print("Error:", e)

  # input & output
#   Generating LALR tables
# calc > 10+5
# 15
# calc > 10/0
# Error: division by zero
# calc > 5+@
# Invalid character: @
# Syntax error at EOF
# None
# calc > 
