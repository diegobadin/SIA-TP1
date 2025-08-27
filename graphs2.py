import os
import argparse

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_results(folder):
    all_files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(".csv")]
    df = pd.concat([pd.read_csv(f) for f in all_files], ignore_index=True)
    return df
def plot_all_metrics(df):
    # Agrupar y calcular media y std
    grouped = df.groupby(["algorithm", "heuristic"]).agg(
        mean_cost=("cost", "mean"),
        std_cost=("cost", "std"),
        mean_expanded=("expanded", "mean"),
        std_expanded=("expanded", "std"),
        mean_frontier=("frontier", "mean"),
        std_frontier=("frontier", "std"),
        mean_time=("duration_sec", "mean"),
        std_time=("duration_sec", "std"),
    ).reset_index()


    # Orden deseado
    algo_order = ["bfs", "dfs", "iddfs", "astar", "greedy"]

    def label_algo(a, h):
        return a if a in ["bfs", "dfs", "iddfs"] else f"{a}-{h}"

    # --------- 1. COST ---------
    plt.figure(figsize=(10,6))
    for heuristic in grouped["heuristic"].unique():
        subset = grouped[grouped["heuristic"] == heuristic]
        lower_error = np.minimum(subset["std_cost"], subset["mean_cost"])
        yerr = [lower_error, subset["std_cost"]]
        bars = plt.bar(
            [label_algo(a, heuristic) for a in subset["algorithm"]],
            subset["mean_cost"],
            yerr=yerr,
            capsize=5,
            label=heuristic
        )
        plt.bar_label(bars, fmt="%.1f", label_type="center", fontsize=8, color="white")
    plt.xticks(
        [label_algo(a, h) for a, h in zip(grouped["algorithm"], grouped["heuristic"])],
        rotation=45, ha="right"
    )
    plt.title("Costo promedio por Algoritmo + Heurística")
    plt.ylabel("Costo (media ± std)")
    plt.tight_layout()
    plt.legend(title="Heurística")
    plt.show()

    # --------- 2. EXPANDED ---------
    plt.figure(figsize=(10,6))
    for heuristic in grouped["heuristic"].unique():
        subset = grouped[grouped["heuristic"] == heuristic]
        lower_error = np.minimum(subset["std_expanded"], subset["mean_expanded"])
        yerr = [lower_error, subset["std_expanded"]]
        bars = plt.bar(
            [label_algo(a, heuristic) for a in subset["algorithm"]],
            subset["mean_expanded"],
            yerr=yerr,
            capsize=5,
            label=heuristic
        )
        plt.bar_label(bars, fmt="%.1f", label_type="center", fontsize=8, color="white")
    plt.yscale("log")
    plt.xticks(
        [label_algo(a, h) for a, h in zip(grouped["algorithm"], grouped["heuristic"])],
        rotation=45, ha="right"
    )
    plt.title("Nodos expandidos promedio")
    plt.ylabel("Expandidos (log, media ± std)")
    plt.tight_layout()
    plt.legend(title="Heurística")
    plt.show()

    # --------- 3. FRONTIER ---------
    plt.figure(figsize=(10,6))
    for heuristic in grouped["heuristic"].unique():
        subset = grouped[grouped["heuristic"] == heuristic]
        lower_error = np.minimum(subset["std_frontier"], subset["mean_frontier"])
        yerr = [lower_error, subset["std_frontier"]]
        bars = plt.bar(
            [label_algo(a, heuristic) for a in subset["algorithm"]],
            subset["mean_frontier"],
            yerr=yerr,
            capsize=5,
            label=heuristic
        )
        plt.bar_label(bars, fmt="%.1f", label_type="center", fontsize=8, color="white")
    plt.yscale("log")
    plt.xticks(
        [label_algo(a, h) for a, h in zip(grouped["algorithm"], grouped["heuristic"])],
        rotation=45, ha="right"
    )
    plt.title("Tamaño de frontera promedio")
    plt.ylabel("Frontera (log, media ± std)")
    plt.tight_layout()
    plt.legend(title="Heurística")
    plt.show()

    # --------- 4. TIME ---------
    plt.figure(figsize=(10,6))
    for heuristic in grouped["heuristic"].unique():
        subset = grouped[grouped["heuristic"] == heuristic]
        lower_error = np.minimum(subset["std_time"], subset["mean_time"])
        yerr = [lower_error, subset["std_time"]]
        bars = plt.bar(
            [label_algo(a, heuristic) for a in subset["algorithm"]],
            subset["mean_time"],
            yerr=yerr,
            capsize=5,
            label=heuristic
        )
        plt.bar_label(bars, fmt="%.1f", label_type="edge", fontsize=8, color="black")
    plt.xticks(
        [label_algo(a, h) for a, h in zip(grouped["algorithm"], grouped["heuristic"])],
        rotation=45, ha="right"
    )
    plt.title("Tiempo de ejecución promedio")
    plt.ylabel("Segundos (media ± std)")
    plt.tight_layout()
    plt.legend(title="Heurística")
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graficar métricas de resultados de algoritmos")
    parser.add_argument("--folder", type=str, default="results",
                        help="Carpeta donde están los CSVs")
    args = parser.parse_args()

    df = load_results(args.folder)
    plot_all_metrics(df)
