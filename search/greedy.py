from search import informed_search


def solve_with_greedy(initial_state, heuristic, goal_positions, board):
    greedy_priority = lambda state, goals, g_val, walls: heuristic(state, goals, walls)
    return informed_search.solve_informed_search(initial_state, greedy_priority, goal_positions, board, None)