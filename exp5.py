# TITLE: Implementation of Bottom up Parser
# AIM: Write a Program to implement Shift Reduce Parser in Python/Java

# Theory:Bottom-up Parsers parses the tree from leaves(bottom) to the root(up). A more general
# form of shift reduce parser is LR parser. It requires some data structures i.e.
# • An input buffer for storing the input string.
# • A stack for storing and accessing the production rules.
# LR parser :
# LR parser is a bottom-up parser for context-free grammar that is very generally used by computer
# programming language compiler and other associated tools. LR parser reads their input from left to
# right and produces a right-most derivation. It is called a Bottom-up parser because it attempts to
# reduce the top-level grammar productions by building up from the leaves. LR parsers are the most
# CLR Parser :
# The CLR parser stands for canonical LR parser.It is a more powerful LR parser.It makes use of
# lookahead symbols. This method uses a large set of items called LR(1) items.The main difference
# between LR(0) and LR(1) items is that, in LR(1) items, it is possible to carry more information in a
# state, which will rule out useless reduction states.This
# LALR Parser :
# LALR Parser is lookahead LR parser. It is the most powerful parser which can handle large classes
# of grammar. The size of CLR parsing table is quite large as compared to other parsing table. LALR
# reduces the size of this table.LALR works similar to CLR. The only difference is , it combines the
# similar states of CLR parsing table into one single state.


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
