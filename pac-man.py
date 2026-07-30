import pygame

import custom_maze

pygame.init()
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

frame_rate = 60

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

screen_background_color = 119, 51, 68

maze = custom_maze.Maze((20, 20), screen.get_size())


class Player(pygame.sprite.Sprite):
    FILL_RATIO = 0.8
    IMAGE_LOADED = [
        pygame.image.load("assets/pac-mam/pac-mac_frame0.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame1.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame2.png").convert_alpha(),
        pygame.image.load("assets/pac-mam/pac-mac_frame3.png").convert_alpha(),
    ]

    def __init__(self, cell_size):
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

        # y, x | + 1 bc the center of the 42 logo is on the center round up
        self.pos = (0, 0)
        self.rect = self.image.get_rect(topleft=(0, 0))
        self.internal_counter = 0

    def draw(self, surface: pygame.Surface):
        surface.blit(
            self.player_assets[
                (self.internal_counter // 5) % len(self.player_assets)
            ],
            ((self.pos), self.rect.size)
        )

    def update(self):
        self.internal_counter += 1


pac_mac = Player(maze.cell_size)

running = True
while running:
    screen.fill((119, 51, 68))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # update
    pac_mac.update()

    # draw
    maze.draw()
    pac_mac.draw(maze.surface)

    screen.blit(maze.surface, maze.rect.topleft)
    pygame.display.update()
    clock.tick(frame_rate)
