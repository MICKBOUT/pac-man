import math
import json

import pygame

from monitor import Monitor
from enum_packman import Menu_name
from button import Button
from texte_zone import Texte, Text_zone
from ghost_anim import Anim


class Menu():
    def __init__(self, windows: pygame.Surface, size: tuple[int, int]) -> None:
        self.windows = windows
        self.size = size
        self.txt_packman = Texte(windows,
                                 50, (255, 204, 1))
        self.txt_rules = Texte(self.windows,
                               20, (255, 204, 1))
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
        self.image_score = pygame.image.load("assets/scene/score.png")
        self.image_rules = pygame.image.load("assets/scene/rules.png")
        self.image_control = pygame.image.load("assets/scene/control.png")
        self.anim = Anim(windows)
        self.anim_pos_x = 0
        self.angle = 40
        self.angle_diff = 2

    def display(self, monitor: Monitor):
        if monitor.windows_resized:
            self.size = self.windows.get_size()
            print(self.size)
            self.b_play = Button(self.windows, "P L A Y", 200, 100,
                                 (self.size[0] / 2 - 100,
                                  self.size[1] / 2 - 150),
                                 10, 30, 90)
            self.b_rule = Button(self.windows, "R U L E S", 200, 100,
                                 (self.size[0] / 2 - 100,
                                  self.size[1] / 2 - 50),
                                 10, 30, 70)
            self.b_scores = Button(self.windows, "S C O R E S", 200, 100,
                                   (self.size[0] / 2 - 100,
                                    self.size[1] / 2 + 50),
                                   10, 30, 70)
        if monitor.menu == Menu_name.Menu.value:
            self.display_menu(monitor)
        elif monitor.menu == Menu_name.Start.value:
            self.start_anim(monitor)
        elif monitor.menu == Menu_name.Play.value:
            monitor.game.game_loop(
                monitor.windows_resized,
                monitor.screen_change,
                monitor.key_press
            )
        elif monitor.menu == Menu_name.Score.value:
            self.display_score()
        elif monitor.menu == Menu_name.rules.value:
            self.display_rules(monitor)

    def start_anim(self, monitor: Monitor) -> None:
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
        if self.anim_pos_x >= self.size[0] + 150:
            monitor.menu = Menu_name.Menu.value

    def display_menu(self, monitor: Monitor) -> None:
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, 0, self.size[0], self.size[1]))
        self.windows.blit(self.image_menu,
                          ((self.size[0] / 2) - 250, (self.size[1] / 16) - 50))
        if self.b_play.add():
            monitor.screen_change = True
            monitor.menu = Menu_name.Play.value
        if self.b_rule.add():
            monitor.menu = Menu_name.rules.value
        if self.b_scores.add():
            monitor.menu = Menu_name.Score.value
        self.anim.add(self.size)

    def display_score(self):
        try:
            with open("score.json", "r") as files:
                dic_score = json.load(files)
        except Exception:
            with open("score.json", "w") as files:
                dic_score = []
        dic_score = sorted(dic_score, key=lambda x: x["score"], reverse=True)
        self.windows.fill((0, 0, 0))
        x = self.size[0] / 32
        y = self.size[1] / 8
        self.windows.blit(self.image_score, (x * 16 - 400, -50))
        if len(dic_score) > 0:
            i = 1
            j = 0
            for dico in dic_score:
                try:
                    txt = f"{5 * j + i}: "\
                          f"{dico["name"]:<11} - {dico["score"]:>5}"
                except Exception:
                    txt = "Are you trying to cheat?"
                self.txt_packman.display_texte(txt,
                                               (6 * x + x * j * 12, y + y * i))
                i += 1
                if i == 6:
                    j += 1
                    i = 1
        if dic_score == []:
            self.txt_packman.display_texte("The score file is empty",
                                           (11 * x, 4 * y))
        with open("score.json", "w") as files:
            json.dump(dic_score, files, indent="\t")

    def display_rules(self, monitor):
        self.windows.fill((0, 0, 0))
        rules = Text_zone(monitor, self.windows)
        rules.add((50, 150), (self.size[0] - 100, self.size[1] - 300))
        self.windows.blit(self.image_rules,
                          ((self.size[0] // 2) - 325, -50))
        self.windows.blit(self.image_control,
                          ((self.size[0] // 2) - 320, self.size[1] // 2 - 100))
