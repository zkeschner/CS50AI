from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    Implication(AKnight, And(AKnave, AKnight)),
    Implication(AKnave, Not(And(AKnight, AKnave)))
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    #A and B cant be a knave and knight
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    #If A is truth, theyre both knaves, but cant be truth since he said hes a knave
    Implication(AKnight, (And(AKnave, BKnave))),
    #If A is lying, he must be knave, therefore Bmust be knight
    Implication(AKnave, Not(And(AKnave, BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    #A and B cant be both knight and knave
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    #If A is a knight, theyre either both knights or knaves (But must be both knights)
    Implication(AKnight, Or(And(AKnight, BKnight), And(BKnave, AKnave))),
    #If A is a knave, they both must be diff (Knight/Knave or vice versa), but (must be knave/knight since a is already knave)
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, AKnave)))),
    #If B is knight, they must be different (A knave, b knight since B already knight)
    Implication(BKnight, Not(Or(And(AKnight, BKnight), And(AKnave, BKnave)))),
    #If B is knave, they must be the same (Both knaves, but then A is lying so must be differnt)
    Implication(BKnave, Or(And(AKnight, BKnight), And(AKnave, BKnave)))
                
                
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    #A/B/C cant be both types
    And(Or(AKnight, AKnave), Not(And(AKnight, AKnave))),
    And(Or(BKnight, BKnave), Not(And(BKnight, BKnave))),
    And(Or(CKnight, CKnave), Not(And(CKnight, CKnave))),
    #If BKnight, A must've said that. Therefore, A either is a knight and is a knave(Impossible), or A is a knave and must be a knight (Also impossible) - B must be knave
    Implication(BKnight, And(
                Implication(AKnight, AKnave),
                Implication(AKnave, Not(AKnave)))),
    #If BKnight, C must be knave as he said
    Implication(BKnight, CKnave),
    #If B is knave, A did not say hes a knave, so must've siad hes a knight. If A is knave, he is lying (checks), or if A is knight he is truthful (Also checks)
    Implication(BKnave, And(
                Implication(AKnight, AKnight),
                Implication(AKnave, AKnave))),
    #If B is lying, C is a knight
    Implication(BKnave, Not(CKnave)),
    #If C is truth, A is knight
    Implication(CKnight, AKnight),
    #If C is knave, A must also be knave
    Implication(CKnave, AKnave)
    
    
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
