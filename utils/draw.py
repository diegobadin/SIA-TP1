import matplotlib.pyplot as plt
import numpy as np

def draw_sokoban(walls, boxes, goals, player):
    """
    state: (no lo uso acá, pero podría ser útil)
    walls, boxes, goals, player -> sets de posiciones (row, col)
    """

    rows = max(r for r, c in walls) + 1
    cols = max(c for r, c in walls) + 1

    # 0 vacío, 1 pared, 2 caja, 3 objetivo, 4 jugador
    grid = np.zeros((rows, cols))

    for r, c in walls:
        grid[r, c] = 1
    for r, c in goals:
        grid[r, c] = 3
    for r, c in boxes:
        grid[r, c] = 2
    pr, pc = player
    grid[pr, pc] = 4

    plt.imshow(grid, cmap="tab20")
    plt.xticks([])
    plt.yticks([])
    plt.show()