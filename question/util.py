from typing import Dict, List

import matplotlib.pyplot as plt
import numpy as np


def plot_benchmark(
        data: Dict[str, Dict[int, List[float]]],
        errors: Dict[str, int]):
    # Construir el gráfico
    _, (fig1, fig2) = plt.subplots(1, 2, figsize=(13, 7))
    for alg, d in data.items():
        fig1.plot(
            sorted(d.keys()),
            [np.mean(v) for v in d.values()],
            label=alg
        )
    fig1.set_ylabel('Segundos en Ejecución Promedio')
    fig1.set_xlabel('Cantidad de Variables')
    fig1.set_title('Tiempo de ejecución de las soluciones analizadas')
    fig1.legend()
    fig1.yaxis.grid(True)

    # Gráfico de cantidad de errores

    fig2.bar(
        errors.keys(),
        errors.values(),
    )
    fig2.set_ylabel('Respuestas incorrectas')
    fig2.set_title(
        f'Cantidad de respuestas incorrectas de {sum((len(l) for l in list(data.values())[0].values()))}')
    fig2.set_xticks = len(errors)
    fig2.set_xticklabels = errors.keys()

    # Save the figure and show
    plt.tight_layout()
    plt.savefig('benchmark.png')
    plt.show()
