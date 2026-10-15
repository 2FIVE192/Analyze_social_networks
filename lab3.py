"""Модель Эрдёша–Реньи G(n, p).

Дано: n = 25, p = 0.45.
Средняя степень вершины по формуле из лекции: c = (n - 1) * p.
"""
import networkx as nx

N = 25
P = 0.45
SEED = 42

# Генерация графа
G = nx.erdos_renyi_graph(N, P, seed=SEED)

# Средняя степень по построенному графу
k_empirical = sum(d for _, d in G.degree()) / N

# Средняя степень по формуле
k_theory = (N - 1) * P

print(f"n = {N}, p = {P}")
print(f"средняя степень по графу:   {k_empirical:.4f}")
print(f"средняя степень по формуле: {k_theory:.4f}")
print(f"абсолютное отклонение:      {abs(k_empirical - k_theory):.4f}")
print(f"относительное отклонение:   {abs(k_empirical - k_theory) / k_theory * 100:.2f} %")
