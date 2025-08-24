def manhattan_distance(initial_state, goal_positions):
    """
    Computes the Manhattan distance heuristic for a Sokoban state.

    The heuristic estimates how close the state is to the goal by summing,
    for each box, the Manhattan distance to the nearest unassigned goal position.

    Parameters:
    - initial_state: a State object representing the current Sokoban board,
      including the positions of the player and all boxes.
    - goal_positions: a set of tuples (row, col) indicating the target positions
      for the boxes.

    Returns:
    - total_distance: int, the sum of minimum Manhattan distances for all boxes
      to the closest remaining goal.

    Notes:
    - Each goal position is assigned to only one box (to avoid double-counting).
    """

    total_distance = 0
    remaining_goals = set(goal_positions)

    for box in initial_state.boxes:
        min_dist = float('inf')
        closest_goal = None
        for goal in remaining_goals:
            dist = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
            if dist < min_dist:
                min_dist = dist
                closest_goal = goal
        total_distance += min_dist
        if closest_goal:
            remaining_goals.remove(closest_goal)

    return total_distance

def euclidean_distance(initial_state, goal_positions):
    """
    Computes the Euclidean distance heuristic for a Sokoban state.

    The heuristic estimates how close the state is to the goal by summing,
    for each box, the Euclidean distance to the nearest unassigned goal position.

    Parameters:
    - initial_state: a State object representing the current Sokoban board,
      including the positions of the player and all boxes.
    - goal_positions: a set of tuples (row, col) indicating the target positions
      for the boxes.

    Returns:
    - total_distance: float, the sum of minimum Euclidean distances for all boxes
      to the closest remaining goal.

    Notes:
    - Each goal position is assigned to only one box (to avoid double-counting).
    """
    total_distance = 0.0
    remaining_goals = set(goal_positions)

    for box in initial_state.boxes:
        min_dist = float('inf')
        closest_goal = None
        for goal in remaining_goals:
            dist = (box[0] - goal[0]) ** 2 + (box[1] - goal[1]) ** 2
            if dist < min_dist:
                min_dist = dist
                closest_goal = goal
        total_distance += min_dist
        if closest_goal:
            remaining_goals.remove(closest_goal)

    return total_distance


def manhattan_linear_conflicts_distance(initial_state, goal_positions):
    # TODO: implement Greedy search with heuristic
    pass

def manhattan_plus_player_distance(initial_state, goal_positions):
    """
       Computes a non-admissible heuristic for a Sokoban state.

       The heuristic estimates how close the state is to the goal by summing:
       1. For each box, the Manhattan distance to the nearest unassigned goal position.
       2. The Manhattan distance from the player to each box.

       Parameters:
       - initial_state: a State object representing the current Sokoban board,
         including the positions of the player and all boxes.
       - goal_positions: a set of tuples (row, col) indicating the target positions
         for the boxes.

       Returns:
       - total_distance: int, the sum of minimum Manhattan distances for all boxes
      to the closest remaining goal plus the sum of distances from the player to all boxes.

       Notes:
       - Each goal position is assigned to only one box (to avoid double-counting).
       - Since it includes the player's distance to each box, it may overestimate the true cost,
         and therefore is non-admissible.
       """
    # Use the already implemented Manhattan distance for boxes to goals
    total_distance = manhattan_distance(initial_state, goal_positions)

    # Distance from player to all boxes
    total_distance += sum(abs(initial_state.player[0] - box[0]) + abs(initial_state.player[1] - box[1]) for box in initial_state.boxes)

    return total_distance