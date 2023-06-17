from pysat.solvers import MinisatGH
from pysat.formula import CNF


def mini_sat_solve(input: CNF):
    '''
    Solucionador de SAT que utiliza una versión del algoritmo de Minisat, 
    disponible públicamente en Github.

    https://github.com/niklasso/minisat
    '''
    with MinisatGH(input) as minisat:
        if not minisat.solve():
            return False

        return list(minisat.get_model())
