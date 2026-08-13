import pygame


class Pac_gum:
    def __init__(self, size, maze):
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

    def draw(self, windows, cell_size):
        x = cell_size // 2
        y = cell_size // 2
        i = 0
        for line in self.lst_pac_gum:
            j = 0
            for pac_gum in line:
                if pac_gum == 1:
                    pygame.draw.circle(windows, (255, 249, 168),
                                       (x + j * cell_size, y + i * cell_size),
                                       5)
                if pac_gum == 2:
                    pygame.draw.circle(windows, (255, 249, 168),
                                       (x + j * cell_size, y + i * cell_size),
                                       12)
                j += 1
            i += 1
