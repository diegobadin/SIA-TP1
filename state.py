class State:
    def __init__(self, player, boxes):
        self.player = player
        self.boxes = frozenset(boxes)  # frozenset so states are hashable

    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes

    def __hash__(self):
        return hash((self.player, self.boxes))

    def __repr__(self):
        return f"State(player={self.player}, boxes={set(self.boxes)})"

    def is_goal_state(self, goal_positions):
        """
        Returns True if all boxes are on the goal positions, False otherwise.
        """
        return self.boxes == goal_positions

    def get_possible_moves(self, walls):
        moves = []
        # Grid directions: up/down = row change, left/right = column change
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right

        for di, dj in directions:
            new_player = (self.player[0] + di, self.player[1] + dj)

            if new_player in walls:
                continue

            if new_player in self.boxes:
                new_box_pos = (new_player[0] + di, new_player[1] + dj)
                # If the box collides with a wall, or with another box, skip
                if new_box_pos in walls or new_box_pos in self.boxes:
                    continue
                new_boxes = frozenset(self.boxes - {new_player} | {new_box_pos})
                moves.append(State(new_player, new_boxes))
            else:
                moves.append(State(new_player, self.boxes))

        return moves
