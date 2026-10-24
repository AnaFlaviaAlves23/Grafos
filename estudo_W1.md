# Estudos de caso — grafos com pesos

Representação: `list` | semente: 42

## 1. Distância e caminho mínimo

**Grafo grafo_W_1** — origem 10

| Destino | Distância | Caminho mínimo |
|---|---|---|
| 20 | 2.38 | 10 -> 2038 -> 5094 -> 2875 -> 4746 -> 8892 -> 3578 -> 2502 -> 4627 -> 4252 -> 9853 -> 9285 -> 1034 -> 20 |
| 30 | 1.72 | 10 -> 2038 -> 2658 -> 682 -> 4045 -> 30 |
| 40 | 2.05 | 10 -> 2038 -> 2658 -> 682 -> 5941 -> 6759 -> 2195 -> 1223 -> 40 |
| 50 | 1.2 | 10 -> 2038 -> 7521 -> 2258 -> 3235 -> 8078 -> 2532 -> 2527 -> 50 |
| 60 | 1.66 | 10 -> 2038 -> 5094 -> 2875 -> 3598 -> 1268 -> 4333 -> 3383 -> 8182 -> 4328 -> 9082 -> 60 |


## 2. Tempo médio de Dijkstra (um vértice → todos)

| Grafo | n | m | k | Sem heap (s) | Com heap (s) | Speedup |
|---|---|---|---|---|---|---|
| grafo_W_1 | 10000 | 209957 | 10 | 3.451598 | 0.151005 | 22.9x |

Tempos em segundos por execução (tempo total de k execuções / k).
