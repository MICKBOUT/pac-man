import pygame


class PacGum:
    def __init__(self, size: int, maze: list[list[int]]):
        self.size = size
        self.lst_pac_gum = []
        for line in maze:
            lst_temps = []
            for numb in line:
                if numb == 15:
                    lst_temps.append(-1)
                else:
                    lst_temps.append(1)
            self.lst_pac_gum.append(lst_temps)
        self.lst_pac_gum[0][0] = 2
        self.lst_pac_gum[0][len(maze[0]) - 1] = 2
        self.lst_pac_gum[len(maze) - 1][0] = 2
        self.lst_pac_gum[len(maze) - 1][len(maze[0]) - 1] = 2

    def draw(self, windows: pygame.Surface, cell_size: int):
        x = cell_size // 2
        y = cell_size // 2
        for i, line in enumerate(self.lst_pac_gum):
            for j, pac_gum in enumerate(line):
                if pac_gum == 1:
                    pygame.draw.circle(
                        windows,
                        (255, 249, 168),
                        (x + j * cell_size, y + i * cell_size),
                        cell_size * 0.10
                    )
                if pac_gum == 2:
                    pygame.draw.circle(
                        windows,
                        (255, 249, 168),
                        (x + j * cell_size, y + i * cell_size),
                        cell_size * 0.20
                    )
