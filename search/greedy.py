from search import informed_search


def greedy_priority(state, heuristic, g_val):
    return heuristic(state, state.goal_positions)


def solve_with_greedy(initial_state, heuristic, goal_positions, board):
    priority_function = lambda state, goals, g_val: heuristic(state, goals)
    return informed_search.solve_informed_search(initial_state, priority_function, goal_positions)