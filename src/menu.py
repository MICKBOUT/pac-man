import math
import json

import pygame

from monitor import Monitor
from enum_pacman import Menu_name
from button import Button
from texte_zone import Texte, Text_zone, Register_txt
from ghost_anim import Anim
from register import register_json
from game import Game


class Menu:
    """Main menu manager handling rendering and user interaction.

    The `Menu` class encapsulates visual elements (background images,
    buttons, animated elements) and navigation logic between menu
    states. It is driven by a `Monitor` instance which stores global
    state such as current menu, score and configuration data.

    Args:
        windows: The `pygame.Surface` where menu elements are drawn.
        size: Tuple `(width, height)` describing the window size.

    Attributes:
        txt_packman: `Texte` helper for large menu text rendering.
        txt_rules: `Texte` helper for rule text rendering.
        bt_*: Several `Button` instances used for menu interaction.
        image_*: Preloaded scene images used in various menu screens.
        anim: `Anim` instance for small decorative animations.
        register: `Register_txt` helper for player name entry screen.
    """

    def __init__(self, windows: pygame.Surface, size: tuple[int, int]) -> None:
        """Initialize visual elements and interactive widgets.

        Loads required images and creates `Button` and text helpers.
        """
        self.windows = windows
        self.size = size
        self.txt_packman = Texte(windows, 50, (255, 204, 1))
        self.txt_rules = Texte(self.windows, 20, (255, 204, 1))
        self._resize_bt()

        self.image_start = pygame.image.load("assets/scene/start_logo.png")
        self.image_menu = pygame.image.load("assets/scene/menu.png")
        self.image_score = pygame.image.load("assets/scene/score.png")
        self.image_rules = pygame.image.load("assets/scene/rules.png")
        self.image_control = pygame.image.load("assets/scene/control.png")
        self.image_register = pygame.image.load("assets/scene/register.png")
        self.anim = Anim(windows)
        self.register = Register_txt(windows)
        self.anim_pos_x = 0
        self.angle = 40
        self.angle_diff = 2
        self.frame = 0

    def _resize_bt(self) -> None:
        self.bt_play = Button(
            self.windows, "P L A Y",
            (self.size[0] // 2, self.size[1] // 2 - 150), 90)
        self.bt_rule = Button(
            self.windows, "R U L E S",
            (self.size[0] // 2, self.size[1] // 2 - 50), 70)
        self.bt_scores = Button(
            self.windows, "S C O R E S",
            (self.size[0] // 2, self.size[1] // 2 + 50), 70)
        self.bt_register = Button(
            self.windows, "R E G I S T E R",
            (self.size[0] // 2, self.size[1] // 2 + 150), 70)
        self.bt_exit = Button(
            self.windows, "E X I T",
            (self.size[0] // 2, self.size[1] // 2 + 250), 70)
        self.bt_exit_to_menu = Button(
            self.windows, "Exit to Menu",
            (self.size[0] // 2, self.size[1] // 2 + 50), 60)
        self.bt_resume_game = Button(
            self.windows, "Resume game",
            (self.size[0] // 2, self.size[1] // 2 - 50), 60)

    def _reset_game(self, monitor: Monitor) -> None:
        """Reset or initialize a new `Game` instance.

        This configures `monitor.game` from the stored configuration and
        routes the monitor's menu state depending on whether the current
        `monitor.score` qualifies for the high score list.

        Args:
            monitor: The `Monitor` instance containing game and UI state.
        """
        monitor.game = Game(
            self.windows,
            (monitor.config_data.width, monitor.config_data.height),
            monitor,
            monitor.config_data.seed
        )
        monitor.windows_resized = True

        if monitor.score < 0:
            monitor.menu = Menu_name.Menu
            monitor.score = 0
            return

        if len(monitor.height_score) == 0:
            min_score = {}
        else:
            min_score = min(monitor.height_score,
                            key=lambda score: score.get("score", 0))
        if (monitor.score > min_score.get("score", 0) or
           len(monitor.height_score) < 10):
            monitor.menu = Menu_name.Register
        else:
            monitor.menu = Menu_name.Menu
            monitor.score = 0

    def display(self, monitor: Monitor) -> None:
        """Route rendering to the appropriate menu screen.

        The function inspects `monitor.menu` and dispatches to the
        corresponding draw/interaction method. It also handles window
        resize events by rebuilding UI widgets.

        Args:
            monitor: The `Monitor` instance driving application state.
        """
        if monitor.windows_resized:
            self._resize_bt()

        if monitor.menu == Menu_name.Menu:
            self.display_menu(monitor)
        elif monitor.menu == Menu_name.Start:
            self.start_anim(monitor)
        elif monitor.menu == Menu_name.Play:
            monitor.game.game_loop(monitor)
        elif monitor.menu == Menu_name.Game_pause:
            self.display_pause_loop(monitor)
        elif monitor.menu == Menu_name.Register:
            self.display_register(monitor)
        elif monitor.menu == Menu_name.Score:
            self.display_score(monitor)
        elif monitor.menu == Menu_name.Rules:
            self.display_rules(monitor)
        elif monitor.menu == Menu_name.Reset_game:
            self._reset_game(monitor)
        elif monitor.menu == Menu_name.Win:
            self.display_win(monitor)

    def start_anim(self, monitor: Monitor) -> None:
        """Render the simple start animation and advance its state.

        Displays a full-screen start logo and a Pac-Man-shaped polygon
        that moves across the screen. When the animation completes the
        `monitor.menu` is set back to `Menu_name.Menu`.

        Args:
            monitor: The `Monitor` instance used to change menu state
                when the animation finishes.
        """
        y = self.size[1] // 2 + 25
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, 0, self.size[0], self.size[1]))
        self.windows.blit(self.image_start, ((self.size[0] // 2) - 400,
                                             (self.size[1] // 2) - 100))
        pygame.draw.rect(self.windows, (0, 0, 0),
                         (0, y - 75, self.anim_pos_x, y))
        points: list[tuple[float, float]] = [(self.anim_pos_x,
                                              self.size[1] // 2 + 25)]
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
            monitor.menu = Menu_name.Menu

    def display_pause_loop(self, monitor: Monitor) -> None:
        """Render the pause menu and handle its button actions.

        Args:
            monitor: The `Monitor` instance controlling game flow.
        """
        monitor.game.pause_loop(monitor)
        if self.bt_exit_to_menu.add():
            monitor.menu = Menu_name.Reset_game
            monitor.score = -1
            monitor.level = 0
        elif self.bt_resume_game.add():
            monitor.menu = Menu_name.Play
            monitor.resize_entity = True

    def display_menu(self, monitor: Monitor) -> None:
        """Draw the main menu screen and process button presses.

        Pressing buttons updates `monitor.menu` to the target state and
        may flag `monitor.resize_entity` when starting gameplay.

        Args:
            monitor: The `Monitor` instance used to update application
                state based on button presses.
        """
        pygame.draw.rect(
            self.windows, (0, 0, 0), (0, 0, self.size[0], self.size[1]))
        self.windows.blit(
            self.image_menu,
            ((self.size[0] // 2) - 250, (self.size[1] / 16) - 50)
        )
        if self.bt_play.add():
            monitor.menu = Menu_name.Play
            monitor.resize_entity = True
        if self.bt_rule.add():
            monitor.menu = Menu_name.Rules
        if self.bt_scores.add():
            monitor.menu = Menu_name.Score
        self.anim.add(self.size)

    def display_score(self, monitor: Monitor) -> None:
        """Render the high score screen and persist changes.

        The method reads the high-score file, displays entries and writes
        back the possibly-truncated/updated list. Errors opening the file
        are surfaced as exceptions.

        Args:
            monitor: The `Monitor` instance containing configuration and
                the highscore filename.
        """
        try:
            with open(monitor.config_data.highscore_filename, "r") as files:
                dic_score = json.load(files)
        except PermissionError:
            raise Exception("Can't open file "
                            f"{monitor.config_data.highscore_filename}")
        except Exception:
            with open(monitor.config_data.highscore_filename, "w") as files:
                dic_score = []
        dic_score = sorted(dic_score, key=lambda x: x.get("score", 0),
                           reverse=True)
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
                self.txt_packman.display_texte(
                    txt, (6 * x + x * j * 12, y + y * i)
                )
                i += 1
                if i == 6:
                    j += 1
                    i = 1
        if dic_score == []:
            self.txt_packman.display_texte("The score file is empty",
                                           (11 * x, 4 * y))
        with open(monitor.config_data.highscore_filename, "w") as files:
            json.dump(dic_score, files, indent="\t")
        self.anim.add(self.size)

    def display_rules(self, monitor: Monitor) -> None:
        """Show game rules and controls.

        Args:
            monitor: The `Monitor` instance (unused but kept for API
                consistency with other display methods).
        """
        self.windows.fill((0, 0, 0))
        rules = Text_zone(self.windows)
        rules.add((50, 150), (self.size[0] - 100, self.size[1] - 300))
        self.windows.blit(self.image_rules,
                          ((self.size[0] // 2) - 325, -50))
        self.windows.blit(self.image_control,
                          ((self.size[0] // 2) - 320, self.size[1] // 2 - 100))

    def display_register(self, monitor: Monitor) -> None:
        """Render registration UI and persist a new high-score entry.

        When the register button is pressed and there is a name entered
        in `monitor.register_txt`, the helper `register_json` is called
        to store the high-score data.

        Args:
            monitor: The `Monitor` instance providing `register_txt` and
                `score` used when saving the entry.
        """
        self.windows.fill((0, 0, 0))
        self.windows.blit(self.image_register,
                          ((self.size[0] // 2) - 275,
                           0))
        self.register.add(
            (self.size[0] // 2 - 200, self.size[1] // 2 - 50),
            (400, 100), monitor)
        if self.bt_register.add() and len(monitor.register_txt):
            register_json(monitor, monitor.score)
            monitor.register_txt = ""
            monitor.score = 0
            monitor.menu = Menu_name.Menu

    def display_win(self, monitor: Monitor) -> None:
        """Display the victory screen and transition back to menu.

        Args:
            monitor: The `Monitor` instance used to reset state after some
                frames have passed.
        """
        self.windows.fill((0, 0, 0))
        self.txt_packman.display_texte(
            "Congratulation", (self.size[0] // 2 - 123, self.size[1] // 2 - 70)
        )
        txt = f"your score is {monitor.score}"
        self.txt_packman.display_texte(
            txt, (self.size[0] // 2 - 8 * len(txt), self.size[1] // 2 - 20)
        )
        self.frame += 1
        if self.frame % 100 == 0:
            monitor.menu = Menu_name.Reset_game
