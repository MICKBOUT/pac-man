from typing import TYPE_CHECKING

from entity.player import PlayerDraw
from entity.ghost import GhostDraw
from entity.pac_gum import PacGum

if TYPE_CHECKING:
    from monitor import Monitor


def collision(
        player: PlayerDraw,
        ghosts: list[Ghost],
        cell_size: int
      ) -> bool:
    py, px = player.get_true_pos(cell_size)
    for ghost in ghosts:
        if ghost.return_home:
            continue
        gy, gx = ghost.get_true_pos(cell_size)
        if (
            (gx < px + cell_size < gx + cell_size and gy == py) or
            (gx < px < gx + cell_size and gy == py) or
            (gy < py + cell_size < gy + cell_size and gx == px) or
            (gy < py < gy + cell_size and gx == px)
        ):
            if ghost.vulnerable:
                ghost.return_home = True
                ghost.go_home()
            else:
                return True
    return False


def collition_pac_gum(
        player: PlayerDraw,
        pac_gum: PacGum,
        monitor: Monitor
      ) -> None:
    x, y = player.pos
    if pac_gum.lst_pac_gum[x][y] == 2:
        monitor.score += monitor.config_data.points_per_super_pacgum
        monitor.super_pac_gum = True
    if pac_gum.lst_pac_gum[x][y] == 1:
        monitor.score += monitor.config_data.points_per_pacgum
    pac_gum.lst_pac_gum[x][y] = 0
    i = 0
    for line in pac_gum.lst_pac_gum:
        if 1 not in line and 2 not in line:
            i += 1
    if (i == len(pac_gum.lst_pac_gum)):
        return True
    return False
