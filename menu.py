from enum_packman import Menu_name
from button import Button
import pygame
import math


class Menu():

    def __init__(self, windows, size):
        self.windows = windows
        self.size = size
        self.txt_packman = Texte(self.windows,
                                 (self.size[0] / 2, self.size[1] / 2),
                                 50, (255, 0, 0))
        self.b_play = Button(self.windows, "P L A Y", 200, 100,
                             (size[0] / 2 - 100, size[1] / 2 - 150),
                             10, 30, 90)
        self.b_rule = Button(self.windows, "R U L E S", 200, 100,
                             (size[0] / 2 - 100, size[1] / 2 - 50),
                             10, 30, 70)
        self.b_scores = Button(self.windows, "S C O R E S", 200, 100,
                               (size[0] / 2 - 100, size[1] / 2 + 50),
                               10, 30, 70)
        self.image_start = pygame.image.load("assets/scene/start_logo.png")
        self.image_menu = pygame.image.load("assets/scene/menu.png")
        self.anim_pos_x = 0
        self.angle = 40
        self.angle_diff = 2

    def display(self, moniteur):
        if moniteur.menu == Menu_name.Menu.value:
            self.display_menu(moniteur)
        if moniteur.menu == Menu_name.Start.value:
            self.start_anim(moniteur)
        if moniteur.menu == Menu_name.Play.value:
            self.display_play(moniteur)

    def start_anim(self, moniteur):
        y = self.size[1] / 2 + 25
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, 0, self.size[0], self.size[1]))
        self.windows.blit(self.image_start, ((self.size[0] / 2) - 400,
                                             (self.size[1] / 2) - 100))
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, y - 75, self.anim_pos_x, y))
        points = [(self.anim_pos_x, self.size[1] / 2 + 25)]
        for angle in range(self.angle, 360 - self.angle + 1):
            x_pac = self.anim_pos_x + 100 * math.cos(math.radians(angle))
            y_pac = y + 100 * math.sin(math.radians(angle))
            points.append((x_pac, y_pac))
        pygame.draw.polygon(self.windows, (255, 204, 1), points)
        self.anim_pos_x += 10
        self.angle -= self.angle_diff
        if self.angle == 0:
            self.angle_diff = -2
        if self.angle == 40:
            self.angle_diff = 2
        if self.anim_pos_x >= self.size[0] + 100:
            moniteur.menu = Menu_name.Menu.value

    def display_menu(self, moniteur):
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, 0, self.size[0], self.size[1]))
        self.windows.blit(self.image_menu,
                          ((self.size[0] / 2) - 250, (self.size[1] / 16) - 50))
        if self.b_play.draw():
            moniteur.menu = Menu_name.Play.value
        if self.b_rule.draw():
            pass
        if self.b_scores.draw():
            self.anim_pos_x = 0
            moniteur.menu = Menu_name.Start.value

    def display_play(self, moniteur):
        self.windows.fill((119, 51, 68))
        moniteur.pacman.update()
        moniteur.maze.draw()
        moniteur.pacman.draw(moniteur.maze.surface)
        self.windows.blit(moniteur.maze.surface, moniteur.maze.rect.topleft)


class Texte():

    def __init__(self, windows, pos, police_size, color=(255, 255, 255)):
        self.windows = windows
        self.pos = pos
        self.police_size = police_size
        self.color = color

    def display_texte(self, texte):
        font = pygame.font.Font(None, self.police_size)
        screen_texte = font.render(texte, True, self.color)
        self.windows.blit(screen_texte, self.pos)
