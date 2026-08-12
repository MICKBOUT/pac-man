def collision(player, lst_ghost, cell_size):
    py, px = player.get_true_pos(cell_size)
    for ghost in lst_ghost:
        gy, gx = ghost.get_true_pos(cell_size)
        if (gx <= px + cell_size and px + cell_size <= gx + cell_size
           and gy == py):
            return True
        if (gx <= px and px <= gx + cell_size
           and gy == py):
            return True
        if (gy <= py + cell_size and py + cell_size <= gy + cell_size
           and gx == px):
            return True
        if (gy <= py and py <= gy + cell_size
           and gx == px):
            return True
    return False
