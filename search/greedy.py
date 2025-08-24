from search import informed_search


def solve_with_greedy(initial_state, heuristic, walls, goal_positions):
    greedy_priority = lambda state, goals, g_val: heuristic(state, goals)
    return informed_search.solve_informed_search(initial_state, greedy_priority, walls, goal_positions)