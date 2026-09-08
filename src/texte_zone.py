import pygame
from typing import Any

from enum_pacman import Txt


class Text_zone:
    """Utility that wraps long text into lines inside a rectangular area.

    The `add()` method lays out the text from `Txt.Rules.value` within
    the rectangle specified by `pos1` and `pos2`, choosing a font size
    suited to the rectangle width and drawing each visible line.
    """

    def __init__(self, windows: pygame.Surface) -> None:
        """Create a `Text_zone` bound to the given surface.

        Args:
            windows: Pygame surface used for drawing.
        """
        self.windows = windows
        self.size = self.windows.get_size()

    def add(self, pos1: tuple[int, int], pos2: tuple[int, int]) -> None:
        """Flow and draw the rules text inside the provided rectangle.

        Args:
            pos1: Top-left corner `(x1, y1)` of the rectangle.
            pos2: Bottom-right corner `(x2, y2)` of the rectangle.
        """
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
    """Small convenience wrapper for Pygame text rendering.

    `display_texte()` renders a single line of text at the requested
    position using the configured font size and color.
    """

    def __init__(self,
                 windows: pygame.Surface,
                 police_size: int,
                 color: tuple[int, int, int] = (255, 255, 255)) -> None:
        """Initialize text helper.

        Args:
            windows: Surface where text will be blitted.
            police_size: Font size to use for rendering.
            color: RGB color tuple for the text.
        """
        self.windows = windows
        self.police_size = police_size
        self.color = color

    def display_texte(self, texte: str, pos: tuple[float, float]) -> None:
        """Render `texte` at `pos` on the associated surface.

        Args:
            texte: Text string to render. An empty string is rendered as a
                single space to ensure a visible glyph region.
            pos: `(x, y)` position where the text is blitted.
        """
        if texte == "":
            texte = " "
        font = pygame.font.Font(None, self.police_size)
        screen_texte = font.render(texte, True, self.color)
        self.windows.blit(screen_texte, pos)


class Register_txt:
    """Simple input box used by the registration screen.

    The `add()` method draws an input rectangle, shows the current
    `monitor.register_txt` text and a blinking caret.
    """

    def __init__(self, windows: pygame.Surface) -> None:
        """Create a `Register_txt` helper bound to `windows`.

        Args:
            windows: Pygame surface used for drawing the input box.
        """
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
        """Draw the registration input box and current text.

        Args:
            pos1: Top-left corner `(x1, y1)` of the input rectangle.
            pos2: Size `(width, height)` of the input rectangle.
            monitor: `Monitor` instance providing `register_txt`.
        """
        x1, y1 = pos1
        x2, y2 = pos2
        pygame.draw.rect(self.windows, (50, 50, 50), (x1, y1, x2, y2), 3)
        pygame.draw.rect(
            self.windows, (70, 70, 70), (x1 + 3, y1 + 3, x2 - 6, y2 - 6))
        self.txt = monitor.register_txt
        nb_cart = len(self.txt)
        if self.frame % 50 <= 25:
            pygame.draw.rect(
                self.windows, (255, 204, 1),
                (x1 + 30 + 18 * nb_cart, y1 + 20, 10, 60)
            )
        self.police.display_texte(self.txt, (x1 + 20, y1 + 35))
        self.frame += 1
