def parse_board_from_file(file_path):
    """
    Parses a Sokoban board file and extracts:
    - walls: positions of walls
    - goal_positions: positions of goal squares
    - player_pos: initial player position
    - box_positions: initial box positions
    """
    walls = set()
    goal_positions = set()
    player_pos = None
    box_positions = set()

    # White spaces doesnt need to be parsed, since walls surround the whole map.
    # If there isnt a wall or blockage, the player can move.
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            row = line.rstrip('\n')
            for j, cell in enumerate(row):
                pos = (i, j)
                if cell == '#':
                    walls.add(pos)
                if cell == '.':
                    goal_positions.add(pos)
                if cell == '@':
                    player_pos = pos
                if cell == '$':
                    box_positions.add(pos)

    return walls, goal_positions, player_pos, box_positions
