import argparse

import pandas as pd
import matplotlib.pyplot as plt
import os

"""
    This script generates plots from algorithm results stored in CSV files.
    
    How to run from the console:
    
    python3 plots_results.py --metric <metric> --folder <csv_folder>
    
    Parameters:
    --metric : the metric to plot. Available options: duration_sec, cost, expanded, frontier
    --folder : folder where the CSV result files are located. Default is "results"
    
    Example:
    python3 plots_results.py --metric duration_sec --folder results
"""

# Load all CSV results
def load_results(folder="results"):
    dfs = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))
            df["board"] = file.split("_results")[0]
            dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# -----------------------------
# Function 1: all the algorithms
# -----------------------------
def plot_metrics(df, metric="duration_sec"):
    if metric not in ["duration_sec", "cost", "expanded", "frontier"]:
        raise ValueError("Métrica inválida")

    boards = df["board"].unique()

    for board in boards:
        subset = df[df["board"] == board]

        plt.figure(figsize=(10, 6))

        bars_labels = []
        bars_values = []

        for idx, row in subset.iterrows():
            if row["algorithm"].lower() in ["greedy", "astar"]:
                label = f"{row['algorithm']} ({row['heuristic']})"
            else:
                label = row["algorithm"]

            bars_labels.append(label)
            bars_values.append(row[metric])

        plt.bar(bars_labels, bars_values, color=plt.cm.tab20.colors[:len(bars_labels)])
        plt.title(f"Board {board} - Métrica: {metric}")
        plt.ylabel(metric.capitalize())
        plt.xlabel("Algoritmo")
        plt.xticks(rotation=45, ha="right")

        unique_values = sorted(subset[metric].unique())
        plt.yticks(unique_values)

        plt.tight_layout()
        plt.show()

# -----------------------------
# Function 2: only Greedy y A*
# -----------------------------
def plot_greedy_astar(df, metric="duration_sec"):
    if metric not in ["duration_sec", "cost", "expanded", "frontier"]:
        raise ValueError("Métrica inválida")

    boards = df["board"].unique()
    for board in boards:
        subset = df[(df["board"] == board) & (df["algorithm"].str.lower().isin(["greedy", "astar"]))]

        if subset.empty:
            continue

        plt.figure(figsize=(10, 6))

        bars_labels = []
        bars_values = []

        for idx, row in subset.iterrows():
            label = f"{row['algorithm']} ({row['heuristic']})"
            bars_labels.append(label)
            bars_values.append(row[metric])

        plt.bar(bars_labels, bars_values, color=plt.cm.tab20.colors[:len(bars_labels)])
        plt.title(f"Board {board} - Solo Greedy y A* ({metric})")
        plt.ylabel(metric.capitalize())
        plt.xlabel("Algoritmo + Heurística")
        plt.xticks(rotation=45, ha="right")

        unique_values = sorted(subset[metric].unique())
        plt.yticks(unique_values)

        plt.tight_layout()
        plt.show()



# ----------- CONSOLE ENTRY -----------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graficar métricas de resultados de algoritmos")
    parser.add_argument("--metric", type=str, default="duration_sec",
                        help="Métrica a graficar: duration_sec, cost, expanded, frontier")
    parser.add_argument("--folder", type=str, default="results",
                        help="Carpeta donde están los CSVs")
    args = parser.parse_args()

    df = load_results(args.folder)
    plot_metrics(df, metric=args.metric)
    plot_greedy_astar(df, metric=args.metric)
