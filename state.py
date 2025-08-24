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


    def is_deadlock(self, new_boxes,new_box_pos, walls, goal_positions):
        row, col = new_box_pos
        # draw_sokoban(walls, self.boxes, goal_positions, self.player)


        # pares de direcciones que forman esquinas
        corner_checks = [
            (directions['U'], directions['R']),
            (directions['R'], directions['D']),
            (directions['D'], directions['L']),
            (directions['L'], directions['U'])
        ]

        for d1, d2 in corner_checks:
            r1, c1 = row + d1[0], col + d1[1]
            r2, c2 = row + d2[0], col + d2[1]
            if (r1, c1) in walls and (r2, c2) in walls:
                return True

        for key, (di, dj) in directions.items():
            neighbor = (row + di, col + dj)
            if neighbor in new_boxes:
                for offset1, offset2 in l_checks[key]:
                    r1, c1 = row + offset1[0], col + offset1[1]
                    r2, c2 = row + offset2[0], col + offset2[1]
                    if (r1, c1) in walls and (r2, c2) in walls:
                        return True

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
                if not self.is_deadlock(new_boxes,new_box_pos,walls,goal_positions) or new_box_pos in goal_positions:
                    moves.append((action, State(new_player, new_boxes)))
            else:
                moves.append((action, State(new_player, self.boxes)))

        return moves



