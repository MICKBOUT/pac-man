from typing import TYPE_CHECKING

from entity.player import PlayerDraw
from entity.ghost import GhostDraw
from entity.pac_gum import PacGum

if TYPE_CHECKING:
    from monitor import Monitor


def collision(
        player: PlayerDraw,
        ghosts: list[GhostDraw],
        cell_size: int,
        monitor: Monitor
      ) -> bool:
    """Detect and handle collisions between the player and ghosts.

    The function computes the true positions of the player and each ghost
    on the grid (using `cell_size`) and checks for overlapping positions.
    If a non-vulnerable ghost collides with the player the function returns
    True to indicate the player has been caught. If a vulnerable ghost
    collides with the player, the ghost is sent home and the player's score
    is increased by the configured `points_per_ghost` value.

    Args:
        player: The `PlayerDraw` instance representing the player.
        ghosts: A list of `GhostDraw` instances currently active in the game.
        cell_size: Size (in pixels) of a single grid cell; used to compute
            true positions for collision checks.
        monitor: The `Monitor` object used to update score and game state.

    Returns:
        True if the player collides with a non-vulnerable ghost (player dies),
        otherwise False.
    """
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
                monitor.score += monitor.config_data.points_per_ghost
            else:
                return True
    return False


def collition_and_win_pacgum(
        player: PlayerDraw,
        pac_gum: PacGum,
        monitor: Monitor
      ) -> bool:
    """Handle pac-gum collection and check for win condition.

    When the player is positioned on a cell containing a pac-gum, this
    function updates the score according to whether the pac-gum is a
    regular pac-gum or a super pac-gum, clears the pac-gum from the grid,
    and sets the `super_pac_gum` flag on the monitor if appropriate.
    It also checks whether all pac-gums have been collected and returns
    True in that case to signal a win.

    Note: The function name contains a historical misspelling
    (`collition` instead of `collision`) and is kept for backward
    compatibility with existing imports.

    Args:
        player: The `PlayerDraw` instance representing the player.
        pac_gum: The `PacGum` instance that stores pac-gum grid state
            (`lst_pac_gum` attribute expected to be a 2D list of ints).
        monitor: The `Monitor` object used to update score and game state.

    Returns:
        True if all pac-gums have been collected (win), otherwise False.
    """
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
