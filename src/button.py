import pygame


class Button:
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
        self.pressed = False
        self.depth = self.DEPTH
        self.window = window
        font = pygame.font.Font(None, font_size)
        self.button_surface = font.render(text, True, self.BUTTON_COLOR)
        self.button_surface_mouseover = font.render(
            text, True, self.COLOR_MOUSEOVER)
        self.rect = self.button_surface.get_rect(center=pos)

    def add(self) -> bool:
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
