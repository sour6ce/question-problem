from dataclasses import dataclass
from typing import Dict, List

from sympy import Symbol
from sympy.logic.boolalg import Boolean


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
