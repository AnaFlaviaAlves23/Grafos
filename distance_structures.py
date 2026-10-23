"""
distance_structures.py

Estruturas que guardam as estimativas de distância usadas pelo Dijkstra.

O algoritmo (dijkstra.py) só conhece a interface DistanceStore:
    get(v)               -> estimativa atual de distância de v
    decrease(v, d)       -> diminui a estimativa de v para d
    pop_min()            -> remove e devolve (v, dist) do vértice de menor
                            estimativa ainda não finalizado (None se acabou)
    distances()          -> lista com as distâncias (índice = vértice)

Assim, o Dijkstra é escrito uma única vez e a forma de guardar as
distâncias e extrair o mínimo é trocada passando outra classe:
    VectorDistances -> vetor, mínimo por varredura linear  (O(n^2 + m))
    HeapDistances   -> heap binário com decrease-key        (O((n + m) log n))

Observação: decrease() só é chamado com valores menores que a estimativa
atual e, como os pesos não são negativos, nunca para um vértice que já foi
removido por pop_min().
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

INF = float("inf")


class DistanceStore(ABC):
    """Interface comum das estruturas de estimativas de distância."""

    def __init__(self, num_vertices: int):
        # Índice 0 não é usado: vértices vão de 1 a num_vertices.
        self._dist: List[float] = [INF] * (num_vertices + 1)

    def get(self, v: int) -> float:
        return self._dist[v]

    def distances(self) -> List[float]:
        return self._dist

    @abstractmethod
    def decrease(self, v: int, new_dist: float) -> None:
        """Define a estimativa de v como new_dist (menor que a atual)."""
        raise NotImplementedError

    @abstractmethod
    def pop_min(self) -> Optional[Tuple[int, float]]:
        """Remove e devolve (vértice, distância) de menor estimativa finita."""
        raise NotImplementedError


class VectorDistances(DistanceStore):
    """Dijkstra sem heap: o mínimo é achado varrendo o vetor inteiro."""

    def __init__(self, num_vertices: int):
        super().__init__(num_vertices)
        self._n = num_vertices
        self._done: List[bool] = [False] * (num_vertices + 1)

    def decrease(self, v: int, new_dist: float) -> None:
        self._dist[v] = new_dist

    def pop_min(self) -> Optional[Tuple[int, float]]:
        dist, done = self._dist, self._done
        melhor, u = INF, -1
        for v in range(1, self._n + 1):
            if not done[v] and dist[v] < melhor:
                melhor, u = dist[v], v
        if u == -1:  # restantes são inalcançáveis
            return None
        done[u] = True
        return u, melhor


class HeapDistances(DistanceStore):
    """
    Heap binário de mínimo com decrease-key eficiente.

    _heap guarda os vértices; _pos[v] é a posição de v em _heap (-1 se v não
    está no heap). Com _pos, diminuir a chave de v custa O(log n), sem
    precisar inserir entradas repetidas.
    """

    def __init__(self, num_vertices: int):
        super().__init__(num_vertices)
        self._heap: List[int] = []
        self._pos: List[int] = [-1] * (num_vertices + 1)

    def decrease(self, v: int, new_dist: float) -> None:
        self._dist[v] = new_dist
        if self._pos[v] == -1:  # ainda não está no heap: insere no fim
            self._heap.append(v)
            self._pos[v] = len(self._heap) - 1
        self._sift_up(self._pos[v])

    def pop_min(self) -> Optional[Tuple[int, float]]:
        heap = self._heap
        if not heap:
            return None
        topo = heap[0]
        ultimo = heap.pop()
        self._pos[topo] = -1
        if heap:
            heap[0] = ultimo
            self._pos[ultimo] = 0
            self._sift_down(0)
        return topo, self._dist[topo]

    def _sift_up(self, i: int) -> None:
        heap, pos, dist = self._heap, self._pos, self._dist
        v = heap[i]
        dv = dist[v]
        while i > 0:
            pai = (i - 1) // 2
            vp = heap[pai]
            if dist[vp] <= dv:
                break
            heap[i] = vp
            pos[vp] = i
            i = pai
        heap[i] = v
        pos[v] = i

    def _sift_down(self, i: int) -> None:
        heap, pos, dist = self._heap, self._pos, self._dist
        tamanho = len(heap)
        v = heap[i]
        dv = dist[v]
        while True:
            filho = 2 * i + 1
            if filho >= tamanho:
                break
            if filho + 1 < tamanho and dist[heap[filho + 1]] < dist[heap[filho]]:
                filho += 1
            vf = heap[filho]
            if dist[vf] >= dv:
                break
            heap[i] = vf
            pos[vf] = i
            i = filho
        heap[i] = v
        pos[v] = i