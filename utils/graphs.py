import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os

"""
    This script generates plots from algorithm results stored in CSV files.

    How to run from the console:

    python3 utils/graphs.py  --metric <metric> --folder <csv_folder>

    Parameters:
    --metric : the metric to plot. Available options: duration_sec, cost, expanded, frontier
    --folder : folder where the CSV result files are located. Default is "results"

    Example:
    python3 utils/graphs.py --metric duration_sec --folder results
"""


# -----------------------------
# Load and aggregate CSV results
# -----------------------------
def load_and_aggregate_results(folder="results"):
    dfs = []
    for file in os.listdir(folder):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, file))

            # el nombre del board arranca con "bX" antes de "_"
            board_name = file.split("_")[0]
            df["board"] = board_name

            dfs.append(df)

    # Juntar todo
    all_data = pd.concat(dfs, ignore_index=True)

    # Agrupar por board + algoritmo + heurística
    grouped = (
        all_data
        .groupby(["board", "algorithm", "heuristic"], dropna=False)
        .agg({
            "duration_sec": "mean",
            "cost": "mean",
            "expanded": "mean",
            "frontier": "mean"
        })
        .reset_index()
    )

    return grouped


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

        for _, row in subset.iterrows():
            if row["algorithm"].lower() in ["greedy", "astar"]:
                label = f"{row['algorithm']} ({row['heuristic']})"
            else:
                label = row["algorithm"]

            bars_labels.append(label)
            bars_values.append(row[metric])

        bars = plt.bar(bars_labels, bars_values, color=plt.cm.tab20.colors[:len(bars_labels)])
        plt.title(f"Board {board} - Metric: {metric}")

        # Eje Y dinámico
        if metric == "duration_sec":
            plt.ylabel("Duration (seconds)")
        else:
            plt.ylabel(metric.capitalize())

        plt.xlabel("Algorithm")
        plt.xticks(rotation=45, ha="right")

        # === Mostrar valores arriba de cada barra ===
        for bar, value in zip(bars, bars_values):
            if metric == "duration_sec":
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{value:.5f}", ha="center", va="bottom", fontsize=9)
            else:
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{int(value)}", ha="center", va="bottom", fontsize=9)

        plt.tight_layout()
        plt.show()


# -----------------------------
# Function 2: only Greedy and A*
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

        for _, row in subset.iterrows():
            label = f"{row['algorithm']} ({row['heuristic']})"
            bars_labels.append(label)
            bars_values.append(row[metric])

        bars = plt.bar(bars_labels, bars_values, color=plt.cm.tab20.colors[:len(bars_labels)])
        plt.title(f"Board {board} - Only Greedy & A* ({metric})")

        # Eje Y dinámico
        if metric == "duration_sec":
            plt.ylabel("Duration (seconds)")
        else:
            plt.ylabel(metric.capitalize())

        plt.xlabel("Algorithm + Heuristic")
        plt.xticks(rotation=45, ha="right")

        # === Mostrar valores arriba de cada barra ===
        for bar, value in zip(bars, bars_values):
            if metric == "duration_sec":
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{value:.5f}", ha="center", va="bottom", fontsize=9)
            else:
                plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                         f"{int(value)}", ha="center", va="bottom", fontsize=9)

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

    df = load_and_aggregate_results(args.folder)
    plot_metrics(df, metric=args.metric)
    plot_greedy_astar(df, metric=args.metric)
