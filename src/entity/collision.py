from entity.player import PlayerDraw
from custom_type import Ghost
from entity.pac_gum import PacGum


def collision(
        player: PlayerDraw,
        ghosts: list[Ghost],
        cell_size: int,
        monotor,
        maze
      ) -> bool:
    py, px = player.get_true_pos(cell_size)
    for ghost in ghosts:
        gy, gx = ghost.get_true_pos(cell_size)
        if (gx < px + cell_size and px + cell_size < gx + cell_size
           and gy == py):
            if ghost.vulnerable:
                ghost.go_home(maze)
                return False
            if ghost.return_home:
                return False
            return True
        if (gx < px and px < gx + cell_size
           and gy == py):
            if ghost.vulnerable:
                ghost.go_home(maze)
                return False
            if ghost.return_home:
                return False
            return True
        if (gy < py + cell_size and py + cell_size < gy + cell_size
           and gx == px):
            if ghost.vulnerable:
                ghost.go_home(maze)
                return False
            if ghost.return_home:
                return False
            return True
        if (gy < py and py < gy + cell_size
           and gx == px):
            if ghost.vulnerable:
                ghost.go_home(maze)
                return False
            if ghost.return_home:
                return False
            return True
    return False


def collition_pac_gum(player: PlayerDraw,
                      pac_gum: PacGum,
                      monitor) -> None:
    x, y = player.pos
    if pac_gum.lst_pac_gum[x][y] == 2:
        monitor.score += 100
        monitor.super_pac_gum = True
    if pac_gum.lst_pac_gum[x][y] == 1:
        monitor.score += 10
    pac_gum.lst_pac_gum[x][y] = 0
