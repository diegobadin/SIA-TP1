import time

def solve_with_dfs(initial_state):
    start_time = time.time()

    stack = [initial_state]
    came_from = {initial_state: (None, None)}  # (parent, action)
    visited = set()
    expanded_nodes_qty = 0

    while stack:
        current_state = stack.pop()

        if current_state in visited:
            continue
        visited.add(current_state)

        expanded_nodes_qty += 1

        if current_state.is_goal_state():
            moves = []
            state = current_state
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
                "frontier_nodes_qty": len(stack),
                "solution": "".join(moves),
                "duration": end_time - start_time
            }

        for action, neighbor in current_state.get_possible_moves():
            if neighbor not in came_from:
                came_from[neighbor] = (current_state, action)
                stack.append(neighbor)

    end_time = time.time()
    return {
        "result": "no solution",
        "cost": None,
        "expanded_nodes_qty": expanded_nodes_qty,
        "frontier_nodes_qty": len(stack),
        "solution": "",
        "duration": end_time - start_time
    }
