from typing import List

from pysat.formula import CNF
from sympy import Symbol
from sympy.logic import And, Not, Or
from sympy.logic.boolalg import is_dnf

from question.formula import QuestionInput


def from_sat_input(formula: List[List[int]] | CNF):
    if isinstance(formula, CNF):
        formula = formula.clauses
    # En lugar de negar la fórmula se aplica DeMorgan directamente y se invierte
    # manualmente la expresión
    qi = QuestionInput(
        # Ahora las cláusulas se unen por disyunción
        Or(
            *[
                # Cada cláusula es una conjunción
                And(
                    *[
                        # Se interpreta el valor entero almacenado para saber que
                        # variable(x_i) es y si está negada
                        Symbol(f'x{v}') if v > 0 else Not(Symbol(f'x{-v}')) for v in clause
                    ]
                ) for clause in formula
            ]
        )
    )
    assert is_dnf(
        qi.formula), f'sympy says that {qi.formula} is not DNF. Is he right?'
    qi.dnf_formula = [[-v for v in clause] for clause in formula]
    return qi
