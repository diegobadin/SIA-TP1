
# '#' = pared, '.' = objetivo, '$' = caja, '*' = caja sobre objetivo
# '@' = jugador, '+' = jugador sobre objetivo, ' ' = espacio vacío

search_algorithms = ["A*", "BFS", "DFS", "IDDFS", "Greedy"]

def calculate_sokoban_solution(board, search_algorithm):
    board = [
        "    #####       ",
        "    #   #       ",
        "    #$  #       ",
        "  ###  $##      ",
        "  #  $ $ #      ",
        "### # ## #   ######",
        "#   # ## #####  ..#",
        "# $  $          ..#",
        "##### ### #@##  ..#",
        "    #     #########",
        "    #######        "
    ]

