from turtledemo.paint import switchupdown
from unittest import case

from state import State
from search import bfs, dfs, iddfs, greedy, astar

# No cambian
# '#' = pared
# '.' = objetivo


# Si cambian
# '@' = jugador
# '$' = caja
# ' ' = espacio vacío

def parse_board_from_file(file_path):
    """
    Parses a Sokoban board file and extracts:
    - walls: positions of walls
    - goal_positions: positions of goal squares
    - player_pos: initial player position
    - box_positions: initial box positions
    """
    walls = set()
    goal_positions = set()
    player_pos = None
    box_positions = set()

    # White spaces doesnt need to be parsed, since walls surround the whole map.
    # If there isnt a wall or blockage, the player can move.
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            row = line.rstrip('\n')
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell == '#':
                    walls.add(pos)
                if cell == '.':
                    goal_positions.add(pos)
                if cell == '@':
                    player_pos = pos
                if cell == '$':
                    box_positions.add(pos)

    return walls, goal_positions, player_pos, box_positions


def solve(file_path, algorithm):
    walls, goal_positions, player_pos, box_positions = parse_board_from_file(file_path)
    initial_state = State(player_pos, box_positions)

    if algorithm == 'bfs':
        return bfs.solve_with_bfs(initial_state, walls, goal_positions)
    elif algorithm == 'dfs':
        return dfs.solve_with_dfs(initial_state, walls, goal_positions)
    elif algorithm == 'iddfs':
        return iddfs.solve_with_iddfs(initial_state, walls, goal_positions)
    elif algorithm == 'greedy':
        return greedy.solve_with_greedy(initial_state, walls, goal_positions)
    elif algorithm == 'astar':
        return astar.solve_with_astar(initial_state, walls, goal_positions)
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

if __name__ == "__main__":
    result = solve('boards/b1.txt', "bfs")

    print("=== Sokoban Solver Result ===")
    print(f"Result: {result['result']}")
    print(f"Cost: {result['cost']}")
    print(f"Expanded Nodes: {result['expanded_nodes_qty']}")
    print(f"Max Frontier Size: {result['frontier_nodes_qty']}")
    #print(f"Solution: {' -> '.join(result['solution']) if result['solution'] else 'No solution'}")
    print(f"Duration: {result['duration']:.4f} seconds")
    print("==============================")
