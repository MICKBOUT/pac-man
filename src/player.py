from typing import Optional

import pygame


class Player(pygame.sprite.Sprite):
    FILL_RATIO = 1

    def __init__(self, cell_size: int = 15) -> None:
        self.image_loaded = [
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame0.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame1.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame2.png").convert_alpha(),
            pygame.image.load(
                "assets/pac-mam/pac-mac_frame3.png").convert_alpha(),
        ]
        self.player_assets = [
                pygame.transform.scale(
                        x,
                        (
                            int(cell_size * self.FILL_RATIO),
                            int(cell_size * self.FILL_RATIO)
                        )
                )
                for x in self.image_loaded
            ]
        self.image: pygame.Surface = self.player_assets[0]

        self.rect: pygame.Rect = self.image.get_rect(topleft=(0, 0))
        self.internal_counter = 0

    def update(self) -> None:
        self.internal_counter += 1

    def draw(
            self,
            surface: pygame.Surface,
            cell_resized: Optional[int] = None
          ) -> None:
        if cell_resized:
            self.player_assets = [
                    pygame.transform.scale(
                            x,
                            (
                                int(cell_resized * self.FILL_RATIO),
                                int(cell_resized * self.FILL_RATIO)
                            )
                    )
                    for x in self.image_loaded
                ]
            self.rect = self.image.get_rect(topleft=(self.rect.topleft))
        surface.blit(
            self.player_assets[
                (self.internal_counter // 5) % len(self.player_assets)
            ],
            self.rect,
        )
