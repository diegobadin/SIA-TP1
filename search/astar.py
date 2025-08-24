from search import informed_search


def a_star_priority(state, heuristic, g_val):
    return g_val + heuristic(state, state.goal_positions)


def solve_with_astar(initial_state, heuristic, goal_positions, board):
    priority_function = lambda state, goals, g_val: g_val + heuristic(state, goals)
    return informed_search.solve_informed_search(initial_state, priority_function, goal_positions)
