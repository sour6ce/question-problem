from itertools import product

from question.formula import QuestionInput


def solve(input: QuestionInput, *, max_iter=1000, max_iter_local=80):
    '''
    Este es un solucionador funciona solo cuando la expresión de entrada es DNF.
    En caso contrario se comporta igual que la solución básica.

    Se basa en representar cada cláusula de manera similar a un número entero en
    binario, como la fórmula es DNF entonces esta es verdadera siempre que
    '''
    if input.dnf_formula is None:
        return basic_solve(input)

    r = Random()

    # Cantidad de variables
    s_vars = set((abs(x) for clause in input.dnf_formula for x in clause))
    vars = sorted(s_vars)
    n = len(vars)
