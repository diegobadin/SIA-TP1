import time

def solve_with_iddfs(initial_state, max_depth=100):
    start_time = time.time()
    expanded_nodes_qty = 0
    frontier_nodes_qty = 0

    # AUX: Depth-Limited Search (DLS)
    def dls(state, depth, came_from, visited):
        nonlocal expanded_nodes_qty
        if state in visited:
            return None
        visited.add(state)
        expanded_nodes_qty += 1
        if state.is_goal_state(state.goal_positions):
            return state
        if depth == 0:
            return None
        for action, neighbor in state.get_possible_moves(state.walls):
            if neighbor not in came_from:
                came_from[neighbor] = (state, action)
                result = dls(neighbor, depth - 1, came_from, visited)
                if result is not None:
                    return result
        return None

    for depth_limit in range(1, max_depth + 1):
        came_from = {initial_state: (None, None)}
        visited = set()
        result_state = dls(initial_state, depth_limit, came_from, visited)
        frontier_nodes_qty = len([s for s in came_from if s not in visited])
        if result_state is not None:
            moves = []
            state = result_state
            while came_from[state][0] is not None:
                parent, action = came_from[state]
                moves.append(action)
                state = parent
            moves.reverse()
            end_time = time.time()
            return {
                "result": "solved",
                "cost": len(moves),
                "expanded_nodes_qty": expanded_nodes_qty,
                "frontier_nodes_qty": frontier_nodes_qty,
                "solution": "".join(moves),
                "duration": end_time - start_time
            }
    end_time = time.time()
    return {
        "result": "no solution",
        "cost": None,
        "expanded_nodes_qty": expanded_nodes_qty,
        "frontier_nodes_qty": frontier_nodes_qty,
        "solution": "",
        "duration": end_time - start_time
    }
