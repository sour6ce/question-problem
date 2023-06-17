from random import Random
from typing import List

import pysat.examples.genhard as satgen
from pysat.formula import CNF
from sympy import Symbol
from sympy.logic import And, Implies, Not, Or
from sympy.logic.boolalg import Boolean

from question.formula import QuestionInput

# Aquí se guardan todos los generadores y parámetros "posibles" de fórmulas de difícil
# resolución que vienen incorporados en PySAT. "posibles" se debe a que debido a la
# velocidad de los solucionadores, las fórmulas que se utilizan para probar no deberían
# exceder las 19 variables.
HARD_GENERATORS = {
    'PHP': {
        # 'build' guarda de cada generador la clase que se utiliza para construirlo
        'build': satgen.PHP,
        # 'avaiable' guarda de cada generador los parámetros que se le pueden pasar
        # de forma que
        'available': [
            (1, 0),
            (1, 1),
            (2, 1),
            (1, 2),
            (2, 2),
            (2, 3)
        ]
    },
    'PAR': {
        'build': satgen.PAR,
        'available': [
            (1,),
            (2,)
        ]
    },
    'GT': {
        'build': satgen.GT,
        'available': [
            (2,),
            (3,),
            (4,)
        ]
    }
}


def generate_hard_sat(index: int) -> CNF | None:
    '''
    Genera fórmulas conocidas por ser difícil de resolver que vienen
    incorporadas en PySAT. Se basan en teoremas clásicos de 
    combinatoria.

    Este generador genera fórmulas para SAT.
    '''
    def formulas():
        # Generador de todas las cominaciones posibles de fórmulas
        for kind in HARD_GENERATORS.values():
            for params in kind['available']:
                yield (kind['build'], params)

    pair = next((v for i, v in enumerate(formulas()) if i == index), None)

    if pair is None:
        return None

    # Lo primero que tiene el par es la clase que construye la fórmula
    # Lo segundo son la tupla con los parámetros
    return pair[0](*pair[1])


def generate_custom_NF(n: int, m: int, seed: int | None = None) -> List[List[int]] | None:
    '''
    Genera fórmulas CNF o DNF (el formato es el mismo) aleatorias con `n` variables y a lo
    sumo `m` cláusulas.

    Este generador genera fórmulas para SAT y para el problema actual.
    '''
    r = Random() if seed is None else Random(seed)

    # Se dividen las probabilidades de variable sin negar, negada y ausente para generar
    # fórmulas que sean más diversas y que no tengan una distribución precisamente uniforme.

    def generate_var(
        var: int,
        w_pos: float,
        w_neg: float,
        w_miss: float
    ) -> int | None:
        '''
        Genera el estado de una variable en una cláusula teniendo en cuenta un peso
        en la probabilidad de cada estado de la variable(positiva, negativa o ausente)
        en la cláusula.
        '''
        return r.choices([var, -var, None], [w_pos, w_neg, w_miss], k=1)[0]

    def generate_clause(
        n: int,
        w_pos: float,
        w_neg: float,
        w_miss: float
    ) -> List[int]:
        '''
        Genera una cláusula con `n` variables teniendo en cuenta el peso en la 
        probabilidad del estado de cada una.
        '''
        return [v for i in range(n) if (v := generate_var(i+1, w_pos, w_neg, w_miss)) is not None]

    def generate_formula(
        n: int,
        m: int,
        w_pos: float,
        w_neg: float,
        w_miss: float
    ) -> List[List[int]]:
        '''
        Genera una fórmula con `n` variables y a lo sumo `m` cláusulas teniendo en cuenta 
        el peso en la probabilidad del estado de cada variable.
        '''
        return [c for _ in range(m) if len((c := generate_clause(n, w_pos, w_neg, w_miss))) != 0]

    # Estos son los pesos en las probabilidades que definen el "tipo de fórmula"
    # a generar
    WEIGHTS = [
        (.8, .1, .1),
        (.1, .8, .1),
        (.1, .1, .8),
        (.6, .3, .1),
        (.1, .6, .3),
        (.3, .1, .6),
        (.1, .3, .6),
        (.6, .1, .3),
        (.3, .6, .1),
        (1/3, 1/3, 1/3),
        (.45, .45, .1),
        (.1, .45, .45),
        (.45, .1, .45)
    ]

    return generate_formula(n, m, *(r.choice(WEIGHTS)))


def generate_tree(n: int, seed: int | None) -> QuestionInput:
    '''
    Genera expresiones booleanas aleatorias en forma de árbol de expresiones
    con `n` variables.m` cláusulas.

    Este generador genera fórmulas para el problema actual.
    '''
    r = Random() if seed is None else Random(seed)

    vars = [Symbol(f'x{i+1}' for i in range(n))]

    def generate_exp(level: int = 0) -> Boolean:
        '''
        Genera un nodo del árbol de expresiones. A medida que se vuelve más 
        profundo es más probable que el nodo sea simplemente el símbolo 
        correspondiente a una variable.
        '''
        k = r.randint(0, 3+level)

        if k > 4:
            return r.choice(vars)
        elif k == 0:
            return Not(generate_exp(level=level+1))
        elif k == 1:
            return And(generate_exp(level=level+1), generate_exp(level=level+1))
        elif k == 2:
            return Or(generate_exp(level=level+1), generate_exp(level=level+1))
        elif k == 3:
            return Implies(
                generate_exp(level=level + 1),
                generate_exp(level=level + 1)
            )
