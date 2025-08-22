import time
from collections import deque

def solve_with_bfs(initial_state, walls, goal_positions):
    start_time = time.time()

    frontier = deque([initial_state])  # BFS uses a queue
    came_from = {initial_state: None}  # Store parent state only
    visited = set()
    expanded_nodes_qty = 0

    while frontier:
        current_state = frontier.popleft()

        if current_state in visited:
            continue
        visited.add(current_state)

        expanded_nodes_qty += 1

        if current_state.is_goal_state(goal_positions):
            # Reconstruct solution path
            moves = []
            state = current_state
            while came_from[state] is not None:
                parent = came_from[state]
                # Compare player positions to infer the move
                dr = state.player[0] - parent.player[0]
                dc = state.player[1] - parent.player[1]
                if dr == -1 and dc == 0:
                    moves.append("U")
                elif dr == 1 and dc == 0:
                    moves.append("D")
                elif dr == 0 and dc == -1:
                    moves.append("L")
                elif dr == 0 and dc == 1:
                    moves.append("R")
                state = parent
            moves.reverse()

            end_time = time.time()
            return {
                "result": "solved",
                "cost": len(moves),
                "expanded_nodes_qty": expanded_nodes_qty,
                "frontier_nodes_qty": len(frontier),
                "solution": "".join(moves),
                "duration": end_time - start_time
            }

        for neighbor in current_state.get_possible_moves(walls):
            if neighbor not in came_from:  # not discovered before
                came_from[neighbor] = current_state
                frontier.append(neighbor)

    end_time = time.time()
    return {
        "result": "no solution",
        "cost": None,
        "expanded_nodes_qty": expanded_nodes_qty,
        "frontier_nodes_qty": len(frontier),
        "solution": "",
        "duration": end_time - start_time
    }
