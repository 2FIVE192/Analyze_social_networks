import statistics
import networkx as nx
import math
import matplotlib.pyplot as plt
# модель Эрдёша–Реньи G(n, p).

# Дано: n = 25, p = 0.45.

# Теория (модель G(n, p)):
#     каждое из C(n, 2) возможных рёбер проводится независимо с вероятностью p;
#     степень вершины ~ Bin(n - 1, p), откуда
#         <k> = p * (n - 1)          -- средняя степень
#         <m> = p * n * (n - 1) / 2  -- среднее число рёбер
#     Для n = 25, p = 0.45:  <k> = 0.45 * 24 = 10.8,  <m> = 135.
N = 25
P = 0.45
SEED = 42

# Теоретические значения
k_theory = P * (N - 1)
m_theory = P * N * (N - 1) / 2
var_theory = (N - 1) * P * (1 - P)  # дисперсия степени отдельной вершины

# Генерация графа и сравнение со средней степенью
G = nx.erdos_renyi_graph(N, P, seed=SEED)

degrees = [d for _, d in G.degree()]
m_empirical = G.number_of_edges()
k_empirical = sum(degrees) / N  # = 2 * m_empirical / N

print(f"n = {N}, p = {P}")
print(f"число рёбер (эмпирическое / теоретическое): {m_empirical} / {m_theory:.2f}")
print(f"средняя степень (эмпирическая / теоретическая): {k_empirical:.4f} / {k_theory:.4f}")
print(f"абсолютное отклонение: {abs(k_empirical - k_theory):.4f}")
print(f"относительное отклонение: {abs(k_empirical - k_theory) / k_theory * 100:.2f} %")

# Усреднение по многим реализациям
TRIALS = 1000
means = []
for i in range(TRIALS):
    H = nx.erdos_renyi_graph(N, P, seed=SEED + i)
    means.append(2 * H.number_of_edges() / N)

k_mean_over_trials = statistics.fmean(means)
print(f"<k> по {TRIALS} реализациям: {k_mean_over_trials:.4f} (теория: {k_theory:.4f})")
print(f"отклонение: {abs(k_mean_over_trials - k_theory):.4f}")

# Распределение степеней и коэффициент кластеризации
degree_counts = {}
for d in degrees:
    degree_counts[d] = degree_counts.get(d, 0) + 1

print("Распределение степеней (эмпирическое / теоретическое, Пуассон):")
for k in sorted(degree_counts):
    empirical_freq = degree_counts[k] / N
    poisson_p = (k_theory ** k) * math.exp(-k_theory) / math.factorial(k)
    print(f"  степень {k:2d}: эмпир. {empirical_freq:.4f}   теор. {poisson_p:.4f}")

clustering_empirical = nx.average_clustering(G)
print()
print(f"коэффициент кластеризации (эмпирический / теоретический = p): "
      f"{clustering_empirical:.4f} / {P:.4f}")


# Визуализация распределений
x_max = max(degrees) + 3
x_range = range(0, x_max)
empirical = [degree_counts.get(k, 0) / N for k in x_range]
poisson = [(k_theory ** k) * math.exp(-k_theory) / math.factorial(k) for k in x_range]

plt.figure(figsize=(8, 5))
plt.bar(x_range, empirical, width=0.6, alpha=0.6, label="эмпирическое")
plt.plot(x_range, poisson, "o-", color="red", label="теоретическое (Пуассон)")
plt.xlabel("степень вершины")
plt.ylabel("частота")
plt.title(f"Распределение степеней, G(n={N}, p={P})")
plt.legend()
plt.grid(alpha=0.3)
plt.show()