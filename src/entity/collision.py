from typing import Any
from entity.player import PlayerDraw


# list[Any = list ghost but each class has a diferent name]
def collision(player: PlayerDraw, lst_ghost: list[Any], cell_size: int):
    py, px = player.get_true_pos(cell_size)
    for ghost in lst_ghost:
        gy, gx = ghost.get_true_pos(cell_size)
        if (gx < px + cell_size and px + cell_size < gx + cell_size
           and gy == py):
            return True
        if (gx < px and px < gx + cell_size
           and gy == py):
            return True
        if (gy < py + cell_size and py + cell_size < gy + cell_size
           and gx == px):
            return True
        if (gy < py and py < gy + cell_size
           and gx == px):
            return True
    return False


def collition_pac_gum(player, pac_gum):
    x, y = player.pos
    pac_gum.lst_pac_gum[x][y] = 0
