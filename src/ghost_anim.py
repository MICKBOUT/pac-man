import math

import pygame


class Anim:
    """Menu animation helper that draws animated ghosts and Pac-Man.

    The class manages loaded frames for normal and vulnerable ghost
    animations and provides `add()` to step the animation and render the
    current frame. The `draw_pacman()` helper draws a chomping Pac-Man
    polygon used alongside the ghost frames.

    Args:
        windows: `pygame.Surface` to draw animations onto.
    """

    def __init__(self, windows: pygame.Surface) -> None:
        """Load animation frames and initialize animation state.

        Attributes initialized include pixel position `x`, animation
        frame counters and parameters controlling the Pac-Man mouth
        animation (`angle`, `angle_diff`).
        """
        self.gif_blue_gost = [
            pygame.image.load("assets/animation/blue_gost/blue_ghost_1.png"),
            pygame.image.load("assets/animation/blue_gost/blue_ghost_2.png")
        ]
        self.gif_vulnerable_gost = [
            pygame.image.load("assets/animation/vulnerable_gost/1.png"),
            pygame.image.load("assets/animation/vulnerable_gost/2.png")
        ]
        self.windows = windows
        self.x = -1000
        self.y = 0
        self.frame = 0
        self.nb_image = 0
        self.direction = 5
        self.angle = 40
        self.angle_diff = 2

    def add(self, size: tuple[int, int]) -> None:
        """Advance animation state and render the current frame.

        Args:
            size: Tuple `(width, height)` representing the window size
                used to position the animation.
        """
        if self.frame % 3 == 0:
            self.nb_image = (self.nb_image + 1) % 2
        if self.x >= size[0] + 1000 or self.x <= -1200:
            self.direction *= -1
        if self.direction > 0:
            self.draw_pacman(size, -1)
            self.windows.blit(self.gif_blue_gost[self.nb_image],
                              (self.x, size[1] - 130))
        elif self.direction < 0:
            self.draw_pacman(size, 1)
            self.windows.blit(self.gif_vulnerable_gost[self.nb_image],
                              (self.x, size[1] - 130))
        self.x += self.direction
        self.frame += 1

    def draw_pacman(self, size: tuple[int, int], direction: int) -> None:
        """Draw a Pac-Man-shaped polygon with a chomping animation.

        Args:
            size: Tuple `(width, height)` representing the window size used
                to position Pac-Man vertically.
            direction: Positive or negative integer indicating facing
                direction; used to flip the mouth orientation.
        """
        center_y = size[1] - 65
        center_x = self.x + 200
        points: list[tuple[float, float]] = [(center_x, center_y)]
        if direction > 0:
            for angle in range(180 + self.angle, 540 - self.angle + 1):
                x_pac = center_x + 65 * math.cos(math.radians(angle))
                y_pac = center_y + 65 * math.sin(math.radians(angle))
                points.append((x_pac, y_pac))
            pygame.draw.polygon(self.windows, (255, 204, 1), points)
        elif direction < 0:
            for angle in range(self.angle, 360 - self.angle + 1):
                x_pac = center_x + 65 * math.cos(math.radians(angle))
                y_pac = center_y + 65 * math.sin(math.radians(angle))
                points.append((x_pac, y_pac))
            pygame.draw.polygon(self.windows, (255, 204, 1), points)
        self.angle -= self.angle_diff
        if self.angle <= 0:
            self.angle_diff = -2
        if self.angle >= 40:
            self.angle_diff = 2
