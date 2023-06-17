from itertools import product
from random import Random
from typing import List

from question.formula import QuestionInput
from question.solvers.basic import solve as basic_solve


def solve(input: QuestionInput, *, max_iter=1000, max_iter_local=80):
    '''
    Este es un solucionador funciona solo cuando la expresión de entrada es DNF.
    En caso contrario se comporta igual que la solución básica.

    Se basa en el algoritmo de búsqueda local GSAT pero una versión sobre
    DNF que busca un conjunto de valores que no satisfaga la expresión.
    '''
    if input.dnf_formula is None:
        return basic_solve(input)

    r = Random()

    # Cantidad de variables
    s_vars = set((abs(x) for clause in input.dnf_formula for x in clause))
    vars = sorted(s_vars)
    n = len(vars)

    def random_sol():
        '''
        Brinda una solución random.
        '''
        return [r.random() > .5 for _ in range(n)]

    current_sol: List[bool] = random_sol()

    def fail_clause(clause: List[int], sol: List[bool]):
        '''
        Evalúa si dada una cláusula y una solución, la solución no satisface
        la cláusula.
        '''
        # Crea un conjunto con las variables de la cláusula
        c = set(clause)
        # Cada index de una solución está asociado a una variable en vars
        for i, v in enumerate(sol):
            # Si la variable correspondiente a i está en True y se encuentra
            # tal cual en la cláusula entonces esta se satisface, de igual
            # manera si está en False y se encuentra negada en la cláusula.
            if (vars[i] if v else -vars[i]) in c:
                return False

        # No concuerda ninguna variable, por tanto la cláusula no se satisface.
        return True

    def fitness(sol: List[bool]):
        '''
        Evalúa el número de cláusulas que no se satisfacen. Se supone que mientras 
        más mejor.
        '''
        return sum(
            (
                1 for clause in input.dnf_formula if fail_clause(clause, sol)
            )
        )

    def change(sol: List[bool]):
        '''
        Cambia el valor de una variable de la solución actual. La variable se escoge 
        de una cláusula aleatoria de las que no están satisfechas.
        '''
        def swap(sol: List[bool], index: int):
            '''
            Da una solución distinta donde el valor de la variable en i está invertido.
            '''
            return [v if i != index else not v for i, v in enumerate(sol)]

        # Cambia cada variable
        changes = [swap(sol, i) for i in range(len(sol))]

        # Comprueba el fitness de cada cambio
        improve = [fitness(c) for c in changes]

        best = max(improve)
        # No puede mejorar
        if best <= fitness(sol):
            return None

        # Obtén el índice de los mejores cambios
        best_index = [i for i, v in enumerate(improve) if v == best]

        # Realiza alguno de los mejores cambios
        return changes[r.choice(best_index)]

    def do_we_have_a_solution(sol: List[bool]):
        '''
        Chequea si estamos ante una solución ya que ninguna de las cláusulas se satisfacen.
        '''
        return all((fail_clause(clause, sol) for clause in input.dnf_formula))

    iters = 0
    local_iter = 0

    while iters < max_iter:
        if do_we_have_a_solution(current_sol):
            return [v if activated else -v for v, activated in zip(vars, current_sol)]

        if local_iter > max_iter_local:
            current_sol = random_sol()
            local_iter = 0
            continue

        current_sol = change(current_sol)

        if current_sol is None:
            current_sol = random_sol()
            local_iter = 0

        iters += 1
        local_iter += 1

    return False
