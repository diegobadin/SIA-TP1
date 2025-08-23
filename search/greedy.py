import heapq
import time


def solve_with_greedy(initial_state, heuristic):
    start_time = time.time()

    frontier = []
    heapq.heappush(frontier, (heuristic(initial_state), initial_state))
    came_from = {initial_state: (None, None)}
    visited = set()
    expanded_nodes_qty = 0

    while frontier:
        _, current_state = heapq.heappop(frontier)

        if current_state in visited:
            continue
        visited.add(current_state)
        expanded_nodes_qty += 1

        if current_state.is_goal_state(goal_positions):
            # Reconstruct solution path
            moves = []
            state = current_state
            while came_from[state][0] is not None:
                parent, action = came_from[state]
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

        for action, neighbor in current_state.get_possible_moves(board):
            if neighbor not in came_from:
                came_from[neighbor] = (current_state, action)
                h = heuristic(neighbor, goal_positions)
                heapq.heappush(frontier, (h, neighbor))

    end_time = time.time()
    return {
        "result": "no solution",
        "cost": None,
        "expanded_nodes_qty": expanded_nodes_qty,
        "frontier_nodes_qty": len(frontier),
        "solution": "",
        "duration": end_time - start_time
    }


