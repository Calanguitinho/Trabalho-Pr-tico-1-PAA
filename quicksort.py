# ============================================================
# Projeto: Análise Experimental do Quicksort
# Descrição: Implementação de variações do Quicksort e avaliação
# de desempenho com métricas (tempo, comparações, trocas).
# ============================================================

import os
import sys
import time
import copy
import math
import csv
import random
import statistics
from collections import defaultdict

import pandas as pd
import matplotlib.pyplot as plt

# Aumenta o limite de recursão para lidar com vetores grandes
sys.setrecursionlimit(100000)

# ============================================================
# Classe de contadores (comparações e trocas)
# ============================================================
class Counters:
    """Classe auxiliar para armazenar métricas de execução."""
    def __init__(self):
        self.comparisons = 0
        self.swaps = 0

    def reset(self):
        self.comparisons = 0
        self.swaps = 0

    def as_dict(self):
        return {"comparisons": self.comparisons, "swaps": self.swaps}


# ============================================================
# Funções utilitárias
# ============================================================
def swap(arr, i, j, counters: Counters):
    """Troca dois elementos do array e atualiza contador."""
    if i != j:
        arr[i], arr[j] = arr[j], arr[i]
        counters.swaps += 1


# ============================================================
# Algoritmos de ordenação
# ============================================================
def insertion_sort(arr, left, right, counters: Counters):
    """Insertion Sort instrumentado (conta comparações e trocas)."""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left:
            counters.comparisons += 1
            if arr[j] > key:
                arr[j + 1] = arr[j]
                counters.swaps += 1
                j -= 1
            else:
                break
        arr[j + 1] = key


def lomuto_partition(arr, low, high, counters: Counters):
    """Partição de Lomuto (pivot = último elemento)."""
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        counters.comparisons += 1
        if arr[j] <= pivot:
            i += 1
            swap(arr, i, j, counters)
    swap(arr, i + 1, high, counters)
    return i + 1


def median_of_three_to_end(arr, low, high, counters: Counters):
    """Escolhe pivô pela mediana de três e o coloca no final (para Lomuto)."""
    mid = (low + high) // 2
    a, b, c = arr[low], arr[mid], arr[high]

    counters.comparisons += 1
    if a > b:
        counters.comparisons += 1
        if b > c:
            median_idx = mid
        else:
            counters.comparisons += 1
            median_idx = high if a > c else low
    else:
        counters.comparisons += 1
        if a > c:
            median_idx = low
        else:
            counters.comparisons += 1
            median_idx = high if b > c else mid

    swap(arr, median_idx, high, counters)


def quicksort_recursive(arr, low, high, counters: Counters):
    """Quicksort recursivo padrão."""
    if low < high:
        p = lomuto_partition(arr, low, high, counters)
        quicksort_recursive(arr, low, p - 1, counters)
        quicksort_recursive(arr, p + 1, high, counters)


def quicksort_hybrid(arr, low, high, counters: Counters, M):
    """Quicksort híbrido: usa Insertion Sort quando subvetor <= M."""
    if low < high:
        if (high - low + 1) <= M:
            insertion_sort(arr, low, high, counters)
            return
        p = lomuto_partition(arr, low, high, counters)
        quicksort_hybrid(arr, low, p - 1, counters, M)
        quicksort_hybrid(arr, p + 1, high, counters, M)


def quicksort_hybrid_median(arr, low, high, counters: Counters, M):
    """Quicksort híbrido com mediana-de-três + Insertion Sort."""
    if low < high:
        if (high - low + 1) <= M:
            insertion_sort(arr, low, high, counters)
            return
        median_of_three_to_end(arr, low, high, counters)
        p = lomuto_partition(arr, low, high, counters)
        quicksort_hybrid_median(arr, low, p - 1, counters, M)
        quicksort_hybrid_median(arr, p + 1, high, counters, M)


# ============================================================
# Funções auxiliares de execução e geração de vetores
# ============================================================
def time_run(func, arr):
    """Executa uma função de ordenação e retorna métricas (tempo, comps, swaps)."""
    arr_copy = copy.deepcopy(arr)
    counters = Counters()
    t0 = time.perf_counter()
    func(arr_copy, 0, len(arr_copy) - 1, counters)
    t1 = time.perf_counter()
    return t1 - t0, counters.comparisons, counters.swaps, arr_copy


def gen_random(n, low=0, high=10**6):
    return [random.randint(low, high) for _ in range(n)]

def gen_sorted(n):
    return list(range(n))

def gen_reverse(n):
    return list(range(n, 0, -1))

def gen_many_duplicates(n, unique_count=5):
    choices = [random.randint(0, 1000) for _ in range(unique_count)]
    return [random.choice(choices) for _ in range(n)]

def gen_worst_case_for_lomuto(n):
    return list(range(n))  # pior caso para Lomuto


# ============================================================
# Busca do melhor M para hibridização
# ============================================================
def find_best_M_for_hybrid(sample_runs=10, M_values=None, n=1000):
    """Busca empiricamente o melhor M para QuickSort híbrido."""
    if M_values is None:
        M_values = list(range(2, 51))

    results = []
    base_arrays = [gen_random(n) for _ in range(sample_runs)]

    for M in M_values:
        times = []
        for arr in base_arrays:
            elapsed, _, _, _ = time_run(
                lambda a, l, h, c: quicksort_hybrid(a, l, h, c, M), arr
            )
            times.append(elapsed)
        results.append((M, statistics.mean(times), statistics.pstdev(times)))

    best = min(results, key=lambda x: x[1])
    df = pd.DataFrame(results, columns=["M", "mean_time", "std_time"])
    return best, df


# ============================================================
# Experimentos principais
# ============================================================
def run_experiments(repeats=5, sizes=[1000, 5000, 10000], M_for_hybrid=None):
    """Executa experimentos para diferentes tamanhos e massas de entrada."""
    generators = {
        "random": gen_random,
        "sorted": gen_sorted,
        "reverse": gen_reverse,
        "many_duplicates": lambda n: gen_many_duplicates(n, 5),
        "worst_for_lomuto": gen_worst_case_for_lomuto
    }

    rows = []
    for n in sizes:
        print(f"\n--- Tamanho {n} ---")
        for gen_name, gen_func in generators.items():
            print(f"Massa: {gen_name}")
            inputs = (
                [gen_func(n) for _ in range(repeats)]
                if gen_name in ("random", "many_duplicates")
                else [copy.deepcopy(gen_func(n)) for _ in range(repeats)]
            )

            algos = {
                "quicksort_recursive": lambda a, l, h, c: quicksort_recursive(a, l, h, c),
                "quicksort_hybrid": lambda a, l, h, c: quicksort_hybrid(a, l, h, c, M_for_hybrid),
                "quicksort_hybrid_median": lambda a, l, h, c: quicksort_hybrid_median(a, l, h, c, M_for_hybrid),
            }

            for algo_name, func in algos.items():
                times, comps, swaps = [], [], []
                for arr in inputs:
                    elapsed, comp, swapc, out = time_run(func, arr)
                    times.append(elapsed); comps.append(comp); swaps.append(swapc)
                    if out != sorted(out):
                        print(f"AVISO: saída não ordenada em {algo_name}, n={n}, massa={gen_name}")

                row = {
                    "n": n, "mass": gen_name, "algo": algo_name,
                    "mean_time": statistics.mean(times),
                    "std_time": statistics.pstdev(times),
                    "mean_comparisons": statistics.mean(comps),
                    "mean_swaps": statistics.mean(swaps),
                }
                print(f"  {algo_name}: {row['mean_time']:.6f}s, comps={row['mean_comparisons']:.0f}, swaps={row['mean_swaps']:.0f}")
                rows.append(row)

    return pd.DataFrame(rows)


# ============================================================
# Função principal
# ============================================================
def main():
    random.seed(42)

    # 1) Busca do melhor M
    print("Buscando M ideal (vetores aleatórios n=1000)...")
    best, df_M = find_best_M_for_hybrid(sample_runs=15, M_values=list(range(2,61)), n=1000)
    best_M, best_time, _ = best
    print(f"Melhor M: {best_M}, tempo médio: {best_time:.6f}s")
    df_M.to_csv("M_search_results.csv", index=False)

    # 2) Experimentos principais
    print("\nExecutando experimentos principais...")
    sizes = [1000, 5000, 10000]
    df_results = run_experiments(repeats=7, sizes=sizes, M_for_hybrid=best_M)
    df_results.to_csv("quicksort_experiment_results.csv", index=False)

    # 3) Gráficos
    # Tempo médio em função do tamanho (massa aleatória)
    fig, ax = plt.subplots(figsize=(8,5))
    for algo in df_results['algo'].unique():
        sub = df_results[(df_results['mass']=="random") & (df_results['algo']==algo)]
        ax.plot(sub['n'], sub['mean_time'], marker='o', label=algo)
    ax.set_title("Tempo médio vs tamanho (massa=random)")
    ax.set_xlabel("n"); ax.set_ylabel("tempo médio (s)"); ax.legend()
    plt.grid(True); plt.tight_layout()
    plt.savefig("tempo_vs_n_random.png"); plt.show()

    # Comparação para maior n
    n_sel = max(sizes)
    df_n = df_results[df_results['n']==n_sel]
    fig2, axes = plt.subplots(1,3, figsize=(15,4))
    axes[0].bar(df_n['algo'], df_n['mean_time']); axes[0].set_title(f"Tempo médio (n={n_sel})")
    axes[1].bar(df_n['algo'], df_n['mean_comparisons']); axes[1].set_title(f"Comparações médias (n={n_sel})")
    axes[2].bar(df_n['algo'], df_n['mean_swaps']); axes[2].set_title(f"Trocas médias (n={n_sel})")
    plt.tight_layout(); plt.savefig(f"metrics_n_{n_sel}.png"); plt.show()

    print("\nExecução finalizada. Arquivos salvos:")
    for f in ["M_search_results.csv", "quicksort_experiment_results.csv",
              "tempo_vs_n_random.png", f"metrics_n_{n_sel}.png"]:
        if os.path.exists(f): print(" -", f)

    return df_M, df_results


# ============================================================
# Execução direta
# ============================================================
if __name__ == "__main__":
    df_M, df_results = main()
