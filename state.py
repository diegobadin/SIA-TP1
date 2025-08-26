directions = {
    "U": (-1, 0),
    "D": (1, 0),
    "L": (0, -1),
    "R": (0, 1)
}

l_checks = {
    "U": [((0, 1), (-1, 1)),  # misma fila - columna derecha + fila arriba- columna derecha
          ((0, -1), (-1, -1))],  # fila arriba - misma columna  + fila  arriba- columna izquierda

    "R": [((-1, 0), (-1, 1)),  # arriba misma + arriba-derecha
          ((1, 0), (1, 1))],  # abajo-misma + abajo-derecha

    "D": [((0, 1), (1, 1)),  # misma-derecha + abajo-derecha
          ((0, -1), (1, -1))],  # misma-izquierda + abajo-izquierda

    "L": [((-1, -1), (-1, 0)),  # arriba-izquierda + arriba-misma
          ((1, -1), (1, 0))],  # abajo-izquierda + abajo-misma
}
from utils.draw import draw_sokoban
class State:
    # Grid directions: up/down = row change, left/right = column change

    def __init__(self, player, boxes):
        self.player = player
        self.boxes = frozenset(boxes)  # frozenset so states are hashable
        self._hash = hash((self.player, self.boxes))
    def __eq__(self, other):
        return self.player == other.player and self.boxes == other.boxes

    def __hash__(self):
        return self._hash

    def __repr__(self):
        return f"State(player={self.player}, boxes={set(self.boxes)})"

    def is_goal_state(self, goal_positions):
        """
        Returns True if all boxes are on the goal positions, False otherwise.
        """
        return self.boxes == goal_positions


    def get_possible_moves(self,walls,goal_positions):
        moves = []

        for action, (di, dj) in directions.items():
            new_player = (self.player[0] + di, self.player[1] + dj)

            if new_player in walls:
                continue

            if new_player in self.boxes:
                new_box_pos = (new_player[0] + di, new_player[1] + dj)
                # If the box collides with a wall, or with another box, skip
                if new_box_pos in  walls or new_box_pos in self.boxes:
                    continue

                new_boxes = frozenset(self.boxes - {new_player} | {new_box_pos})
                moves.append((action, State(new_player, new_boxes)))
            else:
                moves.append((action, State(new_player, self.boxes)))

        return moves



