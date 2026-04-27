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
import copy

# ---------------- Grammar Augmentation ----------------
def grammarAugmentation(rules, nonterminals, start_symbol):
    newRules = []

    newStart = start_symbol + "'"
    while newStart in nonterminals:
        newStart += "'"

    newRules.append([newStart, ['.', start_symbol]])

    for rule in rules:
        lhs, rhs = rule.split("->")
        lhs = lhs.strip()

        for part in rhs.split('|'):
            symbols = part.strip().split()
            newRules.append([lhs, ['.'] + symbols])

    return newRules


# ---------------- Closure ----------------
def findClosure(items):
    closure = items.copy()

    while True:
        new_items = []

        for lhs, rhs in closure:
            if '.' in rhs:
                idx = rhs.index('.')

                if idx + 1 < len(rhs):
                    symbol = rhs[idx + 1]

                    # expand ONLY if non-terminal
                    if symbol in nonterm_userdef:
                        for rule in separatedRulesList:
                            if rule[0] == symbol and rule not in closure:
                                new_items.append(rule)

        if not new_items:
            break

        closure.extend(new_items)

    return closure


# ---------------- Normalize State ----------------
def normalize(state):
    return sorted(state)


# ---------------- GOTO ----------------
def GOTO(state, symbol):
    newState = []

    for lhs, rhs in statesDict[state]:
        if '.' in rhs:
            idx = rhs.index('.')
            if idx + 1 < len(rhs) and rhs[idx + 1] == symbol:
                new_rhs = rhs.copy()
                new_rhs[idx], new_rhs[idx + 1] = new_rhs[idx + 1], '.'
                newState.append([lhs, new_rhs])

    if not newState:
        return

    newState = findClosure(newState)
    newState = normalize(newState)

    # check if already exists
    for s in statesDict:
        if normalize(statesDict[s]) == newState:
            stateMap[(state, symbol)] = s
            return

    new_id = len(statesDict)
    statesDict[new_id] = newState
    stateMap[(state, symbol)] = new_id


# ---------------- Compute GOTO ----------------
def compute_GOTO(state):
    symbols = set()

    for lhs, rhs in statesDict[state]:
        if '.' in rhs:
            idx = rhs.index('.')
            if idx + 1 < len(rhs):
                symbols.add(rhs[idx + 1])

    for sym in symbols:
        GOTO(state, sym)


# ---------------- Generate States ----------------
def generateStates():
    processed = set()

    while True:
        updated = False

        for state in list(statesDict.keys()):
            if state not in processed:
                processed.add(state)
                compute_GOTO(state)
                updated = True

        if not updated:
            break


# ---------------- Print ----------------
def printRules(rules):
    for lhs, rhs in rules:
        print(f"{lhs} -> {' '.join(rhs)}")


def printStates():
    for s in statesDict:
        print(f"\nI{s}:")
        printRules(statesDict[s])


def printGOTO():
    print("\nGOTO Table:\n")
    for (s, sym), target in stateMap.items():
        print(f"GOTO(I{s}, {sym}) = I{target}")


# ---------------- MAIN ----------------
rules = [
    "S -> S + M | M | n",
    "M -> M * P | P | a",
    "P -> ( S ) | id | b"
]

nonterm_userdef = ['S', 'M', 'P']
start_symbol = 'S'

print("\nOriginal Grammar:")
for r in rules:
    print(r)

# augmentation
separatedRulesList = grammarAugmentation(rules, nonterm_userdef, start_symbol)

print("\nAugmented Grammar:")
printRules(separatedRulesList)

# initial state
I0 = findClosure([separatedRulesList[0]])

print("\nClosure I0:")
printRules(I0)

# states
statesDict = {0: normalize(I0)}
stateMap = {}

generateStates()

printStates()
printGOTO()

# To Run Program 
# python filename.py
