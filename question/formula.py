from dataclasses import dataclass
from typing import Dict, List

from sympy import Symbol
from sympy.logic import And, Not, Or
from sympy.logic.boolalg import Boolean, is_dnf


@dataclass
class QuestionInput():
    formula: Boolean | Symbol
    # Una lista con las cláusulas que se unen por disyunción.
    # A su vez cada cláusula es una lista de enteros que representan
    # el índice de la variable que participa en esta. Si el entero es
    # negativo entonces la variable se encuentra negada.
    #
    # Versión DNF del DIMACS utilizado para el SAT en CNF
    dnf_formula: List[List[int]] | None = None

    def test_case(self, case: Dict[str, bool]) -> bool:
        '''
        Evalúa la expresión booleana dado un valor específico para cada variable.
        `O(m)` donde `m` son la cantidad de operaciones que se realizan en la
        expresión.
        '''
        return bool(self.formula.subs(case))

    @staticmethod
    def from_clauses(clauses: List[List[int]]):
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
                    ) for clause in clauses
                ]
            )
        )
        assert is_dnf(
            qi.formula), f'sympy says that {qi.formula} is not DNF. Is he right?'
        qi.dnf_formula = clauses
        return qi
