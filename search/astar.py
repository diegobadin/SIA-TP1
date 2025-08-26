from search import informed_search


def solve_with_astar(initial_state, heuristic, goal_positions, board):
    a_star_priority = lambda state, goals, g_val, walls: g_val + heuristic(state, goals, walls)
    return informed_search.solve_informed_search(initial_state, a_star_priority, goal_positions, board)
