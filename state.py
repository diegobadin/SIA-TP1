class State:
    # Grid directions: up/down = row change, left/right = column change

    def __init__(self, player, boxes, goal_position, walls):
        self.player = player
        self.goal_positions = frozenset(goal_position)
        self.boxes = frozenset(boxes)  # frozenset so states are hashable
        self.walls = frozenset(walls)

    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes

    def __hash__(self):
        return hash((self.player, self.boxes))

    def __repr__(self):
        return f"State(player={self.player}, boxes={set(self.boxes)})"

    def is_goal_state(self):
        """
        Returns True if all boxes are on the goal positions, False otherwise.
        """
        return self.boxes == self.goal_positions

    directions = {
        "U": (-1, 0),
        "D": (1, 0),
        "L": (0, -1),
        "R": (0, 1)
    }

    def is_deadlock(self, new_box_pos):
        row, col = new_box_pos


        # pares de direcciones que forman esquinas
        corner_checks = [
            (self.directions['U'], self.directions['R']),
            (self.directions['R'], self.directions['D']),
            (self.directions['D'], self.directions['L']),
            (self.directions['L'], self.directions['U'])
        ]

        for d1, d2 in corner_checks:
            r1, c1 = row + d1[0], col + d1[1]
            r2, c2 = row + d2[0], col + d2[1]

            if (r1, c1) in self.walls and (r2, c2) in self.walls:
                return True  # box in corner

        return False

    def get_possible_moves(self):
        moves = []

        for action, (di, dj) in self.directions.items():
            new_player = (self.player[0] + di, self.player[1] + dj)

            if new_player in self.walls:
                continue

            if new_player in self.boxes:
                new_box_pos = (new_player[0] + di, new_player[1] + dj)
                # If the box collides with a wall, or with another box, skip
                if new_box_pos in self.walls or new_box_pos in self.boxes:
                    continue

                if not self.is_deadlock(new_box_pos) or new_box_pos in self.goal_positions:
                    new_boxes = frozenset(self.boxes - {new_player} | {new_box_pos})
                    moves.append((action, State(new_player, new_boxes, self.goal_positions, self.walls)))
            else:
                moves.append((action, State(new_player, self.boxes, self.goal_positions, self.walls)))

        return moves



