from search import informed_search


def greedy_priority(state, heuristic, g_val):
    return heuristic(state, state.goal_positions)


def solve_with_greedy(initial_state, heuristic, goal_positions, board):
    return informed_search.solve_informed_search(initial_state, greedy_priority, goal_positions)