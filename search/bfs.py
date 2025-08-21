import time
from collections import deque

def solve_with_bfs(initial_state, walls, goal_positions):
    start_time = time.time()

    frontier = deque([initial_state])  # BFS uses queue
    came_from = {initial_state: None}  # For reconstructing path
    move_from = {initial_state: None}  # Optional: store which move led here
    expanded_nodes_qty = 0

    while frontier:
        current_state = frontier.popleft()
        expanded_nodes_qty += 1

        if current_state.is_goal_state(goal_positions):
            # Reconstruct solution path
            path = []
            state = current_state
            while state is not None:
                path.append(state)
                state = came_from[state]
            path.reverse()

            end_time = time.time()
            return {
                "result": "solved",
                "cost": len(path) - 1,
                "expanded_nodes_qty": expanded_nodes_qty,
                "frontier_nodes_qty": len(frontier),
                #"solution": path,
                "duration": end_time - start_time
            }

        for neighbor in current_state.get_possible_moves(walls):
            if neighbor not in came_from:
                came_from[neighbor] = current_state
                frontier.append(neighbor)

    end_time = time.time()
    return {
        "result": "no solution",
        "cost": None,
        "expanded_nodes_qty": expanded_nodes_qty,
        "frontier_nodes_qty": len(frontier),
        #"solution": [],
        "duration": end_time - start_time
    }
