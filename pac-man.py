import pygame

from menu import Menu
from moniteur import Moniteur
from enum_packman import Menu_name

pygame.init()
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

frame_rate = 60

screen_width = 1280
screen_height = 720
screen = pygame.display.set_mode((screen_width, screen_height))

screen_background_color = 119, 51, 68

menu = Menu(screen, (1280, 720))
moniteur = Moniteur(screen)

running = True
while running:
    menu.display(moniteur)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            moniteur.menu = Menu_name.Menu.value

    pygame.display.update()
    clock.tick(frame_rate)
