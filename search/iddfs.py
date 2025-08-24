import time

def solve_with_iddfs(initial_state, depth_step=1):
    start_time = time.time()
    expanded_nodes_qty = 0

    # AUX: Depth-Limited Search (DLS)
    def dls(state, depth, came_from, visited):
        nonlocal expanded_nodes_qty
        if state in visited:
            return False, None
        visited.add(state)
        expanded_nodes_qty += 1
        if state.is_goal_state():
            return True, state
        if depth == 0:
            return True, None
        any_frontier = False
        for action, neighbor in state.get_possible_moves():
            if neighbor not in came_from:
                came_from[neighbor] = (state, action)
                reached_frontier, result = dls(neighbor, depth - 1, came_from, visited)
                if result is not None:
                    return True, result
                if reached_frontier:
                    any_frontier = True
        return any_frontier, None

    depth_limit = depth_step
    while True:
        came_from = {initial_state: (None, None)}
        visited = set()
        reached_frontier, result_state = dls(initial_state, depth_limit, came_from, visited)
        frontier_nodes_qty = len([s for s in came_from if s not in visited])
        if result_state is not None:
            moves = []
            state = result_state
            while came_from[state][0] is not None:
                parent, _ = came_from[state]
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
                "frontier_nodes_qty": frontier_nodes_qty,
                "solution": "".join(moves),
                "duration": end_time - start_time
            }
        if not reached_frontier:
            end_time = time.time()
            return {
                "result": "no solution",
                "cost": None,
                "expanded_nodes_qty": expanded_nodes_qty,
                "frontier_nodes_qty": frontier_nodes_qty,
                "solution": "",
                "duration": end_time - start_time
            }
        depth_limit += depth_step
