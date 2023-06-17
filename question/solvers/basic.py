from itertools import product

from question.formula import QuestionInput


def solve(input: QuestionInput):
    '''
    Este es un solucionador básico que prueba todas las combinaciones posibles
    en los valores de las variables y chequea así si. Retorna `False` en caso
    de que no exista una combinación de variable que no satisfaga la expresión
    devuelve la combinación en caso contrario.
    '''
    symbols = input.formula.free_symbols

    # Cantidad de variables
    vars = len(symbols)

    # Pero pueden haber variables que no forman parte así que se busca el x_i
    # con el i máximo
    vars = max([int(str(s)[1:]) for s in symbols])

    # Recorre cada combinación posible de valores de verdad para cada variable
    # Son 2^n combinaciones donde n es la cantidad de variables en la expresión.
    for case in product((True, False), repeat=vars):
        result = input.test_case({f'x{i+1}': v for i, v in enumerate(case)})
        if not result:
            return list(case)

    return False
