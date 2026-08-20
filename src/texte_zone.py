import pygame
from typing import Any

from enum_pacman import Txt


class Text_zone:
    def __init__(self, windows: pygame.Surface) -> None:
        self.windows = windows
        self.size = self.windows.get_size()

    def add(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
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


class Texte:

    def __init__(self,
                 windows: pygame.Surface,
                 police_size: int,
                 color: tuple[int, int, int] = (255, 255, 255)) -> None:
        self.windows = windows
        self.police_size = police_size
        self.color = color

    def display_texte(self, texte: str, pos: tuple[float, float]) -> None:
        if texte == "":
            texte = " "
        font = pygame.font.Font(None, self.police_size)
        screen_texte = font.render(texte, True, self.color)
        self.windows.blit(screen_texte, pos)


class Register_txt:

    def __init__(self, windows: pygame.Surface) -> None:
        self.windows = windows
        self.txt = ""
        self.police = Texte(windows, 50, (255, 204, 1))
        self.frame = 0

    def add(
        self,
        pos1: tuple[int, int],
        pos2: tuple[int, int],
        monitor: Any
    ) -> None:
        x1, y1 = pos1
        x2, y2 = pos2
        pygame.draw.rect(self.windows, (50, 50, 50), (x1, y1, x2, y2), 3)
        pygame.draw.rect(self.windows, (70, 70, 70),
                         (x1 + 3, y1 + 3, x2 - 6, y2 - 6))
        self.txt = monitor.register_txt
        nb_cart = len(self.txt)
        if self.frame % 50 <= 25:
            pygame.draw.rect(self.windows, (255, 204, 1),
                             (x1 + 30 + 18 * nb_cart,
                             y1 + 20, 10, 60))
        self.police.display_texte(self.txt, (x1 + 20, y1 + 35))
        self.frame += 1
