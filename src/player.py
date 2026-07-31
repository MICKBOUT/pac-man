import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, cell_size: int) -> None:
        self.FILL_RATIO = 0.8
        self.IMAGE_LOADED = [
            pygame.image.load("assets/pac-mam/pac-mac_frame0.png")
            .convert_alpha(),
            pygame.image.load("assets/pac-mam/pac-mac_frame1.png")
            .convert_alpha(),
            pygame.image.load("assets/pac-mam/pac-mac_frame2.png")
            .convert_alpha(),
            pygame.image.load("assets/pac-mam/pac-mac_frame3.png")
            .convert_alpha(),
        ]
        self.player_assets = [
                pygame.transform.scale(
                        x,
                        (
                            int(cell_size * self.FILL_RATIO),
                            int(cell_size * self.FILL_RATIO)
                        )
                )
                for x in self.IMAGE_LOADED
            ]
        self.image = self.player_assets[0]

        self.rect = self.image.get_rect(topleft=(0, 0))
        self.internal_counter = 0

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(
            self.player_assets[
                (self.internal_counter // 5) % len(self.player_assets)
            ],
            self.rect,
        )

    def update(self) -> None:
        self.internal_counter += 1
