import pygame


class Button:
    def __init__(
            self,
            window: pygame.Surface,
            text: str,
            width: int,
            height: int,
            position: tuple[int | float, int | float],
            depth: int,
            radius: int,
            font_size: int) -> None:

        self.window = window
        self.pressed = False
        self.depth = depth
        self.offset = depth
        self.radius = radius
        self.y: float = float(position[1])
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        int_pos = (int(position[0]), int(position[1]))
        self.rect = pygame.Rect(int_pos, (width, height))
        self.text_surface = self.font.render(text, True, (244, 162, 97))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def add(self) -> bool:
        self.rect.y = int(self.y - self.offset)
        self.text_rect.center = self.rect.center
        self.window.blit(self.text_surface, self.text_rect)
        return self.check_mouse_pressed()

    def check_mouse_pressed(self) -> bool:
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            self.text_surface = self.font.render(self.text, True, (255, 0, 0))
            if pygame.mouse.get_pressed()[0]:
                self.offset = 0
                self.pressed = True
            else:
                self.offset = self.depth
                if self.pressed:
                    self.pressed = False
                    return True
        else:
            self.text_surface = self.font.render(self.text, True,
                                                 (255, 204, 1))
        return False
