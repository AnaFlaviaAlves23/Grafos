"""
dijkstra.py

Algoritmo de Dijkstra escrito uma única vez. A forma como as estimativas de
distância são guardadas e o mínimo é extraído vem de fora (store_class),
uma subclasse de DistanceStore (ver distance_structures.py).
"""

from typing import Dict, List, Optional, Type

from distance_structures import DistanceStore


def dijkstra(graph, start: int, store_class: Type[DistanceStore]) -> Dict:
    """
    Calcula a distância de start a todos os vértices alcançáveis e a árvore
    de caminhos mínimos.

    Retorna {'dist': {v: distância}, 'parent': {v: pai}} apenas com os
    vértices alcançáveis a partir de start (mesmo formato de antes).
    Lança ValueError se o grafo tiver peso negativo.
    """
    graph._check_dijkstra(start)
    n = graph.num_vertices
    store = store_class(n)
    parent: List[Optional[int]] = [None] * (n + 1)

    store.decrease(start, 0.0)
    while True:
        item = store.pop_min()
        if item is None:
            break
        u, d = item
        for w, peso in graph.weighted_neighbors(u):
            nova = d + peso
            if nova < store.get(w):
                store.decrease(w, nova)
                parent[w] = u

    return graph._pack_dijkstra(store.distances(), parent)