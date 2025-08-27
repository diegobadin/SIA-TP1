from state import directions, l_checks
import math


def manhattan_distance(initial_state, goal_positions, walls):
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

    for box in initial_state.boxes:
        if has_deadlocks(initial_state.boxes, box, walls, goal_positions):
            return float('inf')

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

def euclidean_distance(initial_state, goal_positions, walls):
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

    for box in initial_state.boxes:
        if has_deadlocks(initial_state.boxes, box, walls, goal_positions):
            return float('inf')

    total_distance = 0.0
    remaining_goals = set(goal_positions)

    for box in initial_state.boxes:
        min_dist = float('inf')
        closest_goal = None
        for goal in remaining_goals:
            dist = math.sqrt((box[0] - goal[0]) ** 2 + (box[1] - goal[1]) ** 2)
            if dist < min_dist:
                min_dist = dist
                closest_goal = goal
        total_distance += min_dist
        if closest_goal:
            remaining_goals.remove(closest_goal)

    return total_distance

def manhattan_linear_conflicts_distance(initial_state, goal_positions, walls):
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

    for box in initial_state.boxes:
        if has_deadlocks(initial_state.boxes, box, walls, goal_positions):
            return float('inf')

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


def manhattan_plus_player_distance(initial_state, goal_positions, walls):
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
    total_distance = manhattan_distance(initial_state, goal_positions, walls)

    # Distance from player to all boxes
    total_distance += sum(abs(initial_state.player[0] - box[0]) + abs(initial_state.player[1] - box[1]) for box in initial_state.boxes)

    return total_distance




def has_deadlocks(new_boxes, new_box_pos, walls, goal_positions):

    if new_box_pos in goal_positions:
        return False

    row, col = new_box_pos

    corner_checks = [
        (directions['U'], directions['R']),
        (directions['R'], directions['D']),
        (directions['D'], directions['L']),
        (directions['L'], directions['U'])
    ]

    # corner check
    for d1, d2 in corner_checks:
        r1, c1 = row + d1[0], col + d1[1]
        r2, c2 = row + d2[0], col + d2[1]
        if (r1, c1) in walls and (r2, c2) in walls:
            return True

    # box next to box with walls
    for key, (di, dj) in directions.items():
        neighbor = (row + di, col + dj)
        if neighbor in new_boxes:
            for offset1, offset2 in l_checks[key]:
                r1, c1 = row + offset1[0], col + offset1[1]
                r2, c2 = row + offset2[0], col + offset2[1]
                if (r1, c1) in walls and (r2, c2) in walls:
                    return True

    # wall along row or column with no goals
    for key, (di, dj) in directions.items():
        neighbor = (row + di, col + dj)

        if neighbor in walls:
            if key in ["U", "D"]:
                wall_row = [(row + di, c) for c in range(min(w[1] for w in walls), max(w[1] for w in walls) + 1)]
                same_row = [(row, c) for c in range(min(w[1] for w in walls), max(w[1] for w in walls) + 1)]
                if not any((row, c) in goal_positions for (_, c) in same_row) and all(
                        pos in walls for pos in wall_row):
                    return True

            if key in ["L", "R"]:
                wall_col = [(r, col + dj) for r in range(min(w[0] for w in walls), max(w[0] for w in walls) + 1)]
                same_col = [(r, col) for r in range(min(w[0] for w in walls), max(w[0] for w in walls) + 1)]
                if not any((r, col) in goal_positions for (r, _) in same_col) and all(
                        pos in walls for pos in wall_col):
                    return True
    return False
