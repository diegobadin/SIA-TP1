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
    """
    Manhattan distance + Linear Conflicts heuristic for Sokoban.

    This heuristic extends Manhattan distance by adding a penalty
    for linear conflicts:
    - If two boxes are in the same row (or column) and their assigned goals
      are also in that row (or column), but the goals are in reversed order
      compared to the boxes, then a conflict occurs.
    - Each conflict adds +2 to the heuristic.

    Returns:
    - heuristic_value: int, Manhattan distance plus 2 times the number of conflicts.
    """
    total_distance, box_to_goal = detail_manhattan_distance(initial_state, goal_positions)

    conflicts = 0

    for row in set(b[0] for b in box_to_goal):
        row_boxes = [(box, goal) for box, goal in box_to_goal.items() if box[0] == row and goal[0] == row]
        row_boxes.sort(key=lambda x: x[0][1])
        for i in range(len(row_boxes)):
            for j in range(i + 1, len(row_boxes)):
                if row_boxes[i][1][1] > row_boxes[j][1][1]:
                    conflicts += 1

    for col in set(b[1] for b in box_to_goal):
        col_boxes = [(box, goal) for box, goal in box_to_goal.items() if box[1] == col and goal[1] == col]
        col_boxes.sort(key=lambda x: x[0][0])
        for i in range(len(col_boxes)):
            for j in range(i + 1, len(col_boxes)):
                if col_boxes[i][1][0] > col_boxes[j][1][0]:
                    conflicts += 1

    return total_distance + 2 * conflicts

def detail_manhattan_distance(initial_state, goal_positions):
    """
    Same as manhettan_distance but also return box_to_goal
    """

    total_distance = 0
    remaining_goals = set(goal_positions)
    box_to_goal = {}

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
            box_to_goal[box] = closest_goal
            remaining_goals.remove(closest_goal)

    return total_distance, box_to_goal