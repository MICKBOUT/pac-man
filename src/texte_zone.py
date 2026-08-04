import pygame

from enum_packman import Txt


class Text_zone():
    def __init__(self, monitor, windows):
        self.windows = windows
        self.monitor = monitor
        self.size = self.windows.get_size()

    def add(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        x1, x2 = sorted((x1, x2))
        y1, y2 = sorted((y1, y2))
        width = x2 - x1
        font_size = max(10, width // 75 + 10)
        text = Texte(self.windows, font_size, (255, 204, 1))
        font = pygame.font.Font(None, font_size)
        words = Txt.Rules.value.split()
        lines = []
        current_l = ""
        for word in words:
            test_line = word if current_l == "" else current_l + " " + word

            if font.size(test_line)[0] <= width:
                current_l = test_line
            else:
                lines.append(current_l)
                current_l = word
        if current_l:
            lines.append(current_l)
        line_height = font.get_linesize()
        for i, line in enumerate(lines):
            y = y1 + i * line_height

            if y + line_height > y2:
                break
            text.display_texte(line, (x1, y))


class Texte():

    def __init__(self, windows, police_size, color=(255, 255, 255)):
        self.windows = windows
        self.police_size = police_size
        self.color = color

    def display_texte(self, texte, pos):
        font = pygame.font.Font(None, self.police_size)
        screen_texte = font.render(texte, True, self.color)
        self.windows.blit(screen_texte, pos)
