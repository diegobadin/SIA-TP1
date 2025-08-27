#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path

# === Configuración ===
BOARDS_DIR = Path("boards")
RESULTS_DIR = Path("results")

ALGORITHMS_NO_HEURISTICS = ["bfs", "dfs", "iddfs"]
ALGORITHMS_HEURISTICS = ["greedy", "astar"]

HEURISTICS = ["manhattan", "euclidean", "linear_conflict", "manhattan_player"]

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

if len(sys.argv) < 2:
    print(f"Uso: {sys.argv[0]} board1.txt [board2.txt ...]")
    sys.exit(1)

for board_path in sys.argv[1:]:
    board = Path(board_path)
    board_name = board.stem

    print(f"▶️ Ejecutando algoritmos para board: {board_name}")

    for version in range(5):  # v0 a v4
        csv_file = RESULTS_DIR / f"{board_name}_v{version}_results.csv"

        with csv_file.open("w") as f:
            f.write("board,algorithm,heuristic,result,cost,expanded,frontier,duration_sec,solution\n")

        # Algoritmos sin heurística
        for alg in ALGORITHMS_NO_HEURISTICS:
            subprocess.run(
                [sys.executable, "main.py", str(board), alg, "--csv"],
                stdout=open(csv_file, "a"),
                check=True
            )

        # Algoritmos con heurística
        for alg in ALGORITHMS_HEURISTICS:
            for heur in HEURISTICS:
                subprocess.run(
                    [sys.executable, "main.py", str(board), alg, heur, "--csv"],
                    stdout=open(csv_file, "a"),
                    check=True
                )

        print(f"✅ Resultados v{version} guardados en {csv_file}")
