import sys
from state import State
from search import bfs, dfs, iddfs, greedy, astar
from utils import heuristics
from utils.parser import parse_board_from_file


def solve(file_path, algorithm, heuristic=heuristics.manhattan_distance):
    walls, goal_positions, player_pos, box_positions = parse_board_from_file(file_path)
    initial_state = State(player_pos, box_positions)

    if algorithm == 'bfs':
        return bfs.solve_with_bfs(initial_state,walls,goal_positions)
    elif algorithm == 'dfs':
        return dfs.solve_with_dfs(initial_state,walls,goal_positions)
    elif algorithm == 'iddfs':
        return iddfs.solve_with_iddfs(initial_state,walls,goal_positions)
    elif algorithm == 'greedy':
        return greedy.solve_with_greedy(initial_state, heuristic, walls, goal_positions)
    elif algorithm == 'astar':
        return astar.solve_with_astar(initial_state, heuristic,walls,  goal_positions)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

"""
    # Compatible with Python 3.10+ 
    match algorithm:
        case 'bfs': return bfs.solve_with_bfs(initial_state, walls, goal_positions)
        case 'dfs': return dfs.solve_with_dfs(initial_state, walls, goal_positions)
        case 'iddfs': return iddfs.solve_with_iddfs(initial_state, walls, goal_positions)
        case 'greedy': return greedy.solve_with_greedy(initial_state, walls, goal_positions)
        case 'astar': return astar.solve_with_astar(initial_state, walls, goal_positions)
        case _: raise ValueError(f"Unknown algorithm: {algorithm}")
"""


def get_heuristic_function(name: str):
    heuristics_map = {
        "manhattan": heuristics.manhattan_distance,
        "euclidean": heuristics.euclidean_distance,
        "linear_conflict": heuristics.manhattan_linear_conflicts_distance,
        "manhattan_player":heuristics.manhattan_linear_conflicts_distance
    }

    if name not in heuristics_map:
        raise ValueError(f"Heuristic '{name}' not recognized. Options: {list(heuristics_map.keys())}")

    return heuristics_map[name]

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("\033[91mUsage: python main.py <board_file_path> <algorithm>\033[0m")
        sys.exit(1)

    board_file_path = sys.argv[1]    # first argument: file path
    algorithm = sys.argv[2]          # second argument: bfs, dfs, etc.
    if len(sys.argv) > 3:
        heuristic = sys.argv[3]      # third argument: manhattan, euclidean, linear_conflict, manhattan_player
    else:
        heuristic = "manhattan"


    result = solve(board_file_path, algorithm, get_heuristic_function(heuristic))

    print("=== Sokoban Solver Result ===")
    print(f"Result: {result['result']}")
    print(f"Cost: {result['cost']}")
    print(f"Expanded Nodes: {result['expanded_nodes_qty']}")
    print(f"Max Frontier Size: {result['frontier_nodes_qty']}")
    print(f"Solution: {result['solution'] if result['solution'] else 'No solution'}")
    print(f"Duration: {result['duration']:.4f} seconds")
    print("==============================")
