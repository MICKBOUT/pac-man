import pygame


class Button:
    """A text button with mouseover and click detection.

    Attributes:
        COLOR_MOUSEOVER: Text color when the mouse is over the button.
        BUTTON_COLOR: Default text color for the button.
        DEPTH: Vertical offset used to render a pressed appearance.

    Args:
        window: `pygame.Surface` where the button will be drawn.
        text: Label text to render on the button.
        pos: `(x, y)` center position on `window` for the button.
        font_size: Font size used to render the label.
    """

    COLOR_MOUSEOVER = (255, 0, 0)
    BUTTON_COLOR = (255, 204, 1)
    DEPTH = 10

    def __init__(
        self,
        window: pygame.Surface,
        text: str,
        pos: tuple[int, int],
        font_size: int,
      ) -> None:
        """Create a `Button` and prepare rendered label surfaces.

        The constructor pre-renders two label surfaces (normal and
        mouseover) and computes the bounding `rect` used for hit tests.
        """
        self.pressed = False
        self.depth = self.DEPTH
        self.window = window
        font = pygame.font.Font(None, font_size)
        self.button_surface = font.render(text, True, self.BUTTON_COLOR)
        self.button_surface_mouseover = font.render(
            text, True, self.COLOR_MOUSEOVER)
        self.rect = self.button_surface.get_rect(center=pos)

    def add(self) -> bool:
        """Draw the button and return True when a click is released.

        The method should be called each frame. When the mouse is over the
        button it draws the mouseover surface and tracks mouse button
        presses. It returns True once when a full click (press then
        release) is detected while over the button.

        Returns:
            True if the button was clicked (press and release detected),
            otherwise False.
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.window.blit(self.button_surface_mouseover, (
                self.rect.x, self.rect.y + self.depth))
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                self.pressed = False
                return True
        else:
            self.window.blit(self.button_surface, self.rect)
            self.pressed = False
        return False
