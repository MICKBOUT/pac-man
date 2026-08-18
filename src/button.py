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
        self.window = window
        self.text = text
        self.depth = self.DEPTH
        self.pressed = False
        self.font = pygame.font.Font(None, font_size)
        self.button_surface = self.font.render(text, True, self.BUTTON_COLOR)
        self.button_surface_mouseover = self.font.render(
            self.text, True, self.COLOR_MOUSEOVER)
        self.rect = self.button_surface.get_rect(center=pos)

    def add(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.window.blit(self.button_surface_mouseover, (
                self.rect.x, self.rect.y + self.depth))
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
            elif self.pressed:
                return True
        else:
            self.window.blit(self.button_surface, self.rect)
            self.pressed = False
        return False
