#!/bin/bash

BOARDS_DIR="boards"
RESULTS_DIR="results"

ALGORITHMS_NO_HEURISTICS=("bfs" "dfs" "iddfs")
ALGORITHMS_HEURISTICS=("greedy" "astar")

HEURISTICS=("manhattan" "euclidean" "linear_conflict" "manhattan_player")

# === Create folder if it does not already exists ===
mkdir -p $RESULTS_DIR

if [ $# -eq 0 ]; then
    echo "Uso: $0 board1.txt [board2.txt ...]"
    exit 1
fi

# === Principal loop ===
for board in "$@"; do
    board_name=$(basename "$board" .txt)
    csv_file="$RESULTS_DIR/${board_name}_results.csv"

    echo "▶️ Ejecutando algoritmos para board: $board_name"
    echo "board,algorithm,heuristic,result,cost,expanded,frontier,duration_sec" > $csv_file

    # Without heuristic algorithms
    for alg in "${ALGORITHMS_NO_HEURISTICS[@]}"; do
        python3 main.py "$board" "$alg" --csv >> $csv_file
    done

    # With heuristic algorithms
    for alg in "${ALGORITHMS_HEURISTICS[@]}"; do
        for heur in "${HEURISTICS[@]}"; do
            python3 main.py "$board" "$alg" "$heur" --csv >> $csv_file
        done
    done

    echo "✅ Resultados guardados en $csv_file"
done