import sys
import pygame
import logging
from enum import Enum, auto
from random import randint

level = logging.DEBUG
# level = logging.INFO
# level = logging.ERROR
# level = logging.FATAL

pygame.init()
sounds = True

TICK_SPEED = 75

logging.basicConfig(format="%(levelname)s:%(name)s >> %(message)s",
                    level=level)


class PipelineBackground:
    def __init__(self, game) -> None:
        self.speed = TICK_SPEED
        self.pipeline = game.assets.pipeline
        self.pipeline2 = game.assets.pipeline2

        self.pipeline_y = 0
        self.pipeline2_y = 1080

    def pipeline_drawing(self, game) -> int:
        self.pipeline_y += self.speed
        self.pipeline2_y += self.speed

        if self.pipeline_y >= 1080:
            self.pipeline_y = -1080
            logging.debug(f"FPS: {game.clock.get_fps():.2f}")
        if self.pipeline2_y >= 1080:
            self.pipeline2_y = -1080

        game.screen.blit(self.pipeline, (0, self.pipeline_y))
        game.screen.blit(self.pipeline2, (0, self.pipeline2_y))

        return 1


class GameStates(Enum):
    mainMenu = auto()
    playMenu = auto()


class Menu:
    def __init__(self):
        self.last_stage = None


class Assets:
    def __init__(self) -> None:
        self.pipeline = pygame.image.load(
            "assets/backgrounds/pipeline.png").convert_alpha()
        self.pipeline2 = pygame.image.load(
            "assets/backgrounds/pipeline2.png").convert_alpha()
        self.play = pygame.image.load(
            "assets/buttons/play.png").convert_alpha()
        self.quit = pygame.image.load(
            "assets/buttons/quit.png").convert_alpha()
        self.ultrapy = pygame.image.load(
            "assets/text/ultrapy.png").convert_alpha()
        self.blackbox = pygame.image.load(
            "assets/backgrounds/blackbox.png").convert_alpha()
        self.blackbox_small = pygame.image.load(
            "assets/backgrounds/blackbox_small.png").convert_alpha()

        self.prelude = pygame.image.load(
            "assets/buttons/prelude.png").convert_alpha()
        self.act1 = pygame.image.load(
            "assets/buttons/act1.png").convert_alpha()

        self.v1 = pygame.image.load(
            "assets/characters/v1.png").convert_alpha()


class Fonts:
    def __init__(self) -> None:
        self.fontBold = pygame.font.SysFont('fonts/ultrafont.ttf', 100,
                                            bold=True)
        self.fontTitle = pygame.font.SysFont('fonts/ultrafont.ttf', 100)
        self.font20 = pygame.font.SysFont('fonts/ultrafont.ttf', 20)
        self.font30 = pygame.font.SysFont('fonts/ultrafont.ttf', 30)
        self.font45 = pygame.font.SysFont('fonts/ultrafont.ttf', 45)


class Sounds:
    def __init__(self) -> None:
        try:
            pygame.mixer.music.load("sounds/mainmenu.ogg")
            self.slam = pygame.mixer.Sound("sounds/slam.mp3")
            self.dash = pygame.mixer.Sound("sounds/dash.mp3")
            self.jump = pygame.mixer.Sound("sounds/jump.mp3")
            self.sound_working = True
        except Exception:
            self.sound_working = False
            return

        return


class KeyEventHandler:
    def __init__(self) -> None:
        return

    def handle(self, game, event) -> int:
        if event.key == pygame.K_ESCAPE:
            game.menu = not game.menu

        if game.inlevel and game.sounds.sound_working:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                sounds.slam.play()
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                sounds.dash.play()
            if event.key == pygame.K_SPACE:
                sounds.jump.play()

        return 0


class EventHandler:
    def __init__(self) -> None:
        self.key_events = KeyEventHandler()
        return

    def handle(self, game, event) -> int:
        if event.type == pygame.QUIT:
            game.running = False
        elif event.type == pygame.KEYDOWN:
            self.key_events.handle(game, event)

        return 0


class mainMenu:
    def __init__(self):
        self.submenu = 0
        self.id = "Main Menu"

    def create_menu_surface(self, game):
        menu_surf = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        mouse_x, mouse_y = pygame.mouse.get_pos()

        play_button = game.assets.play
        play_button_rect = play_button.get_rect(
            center=menu_surf.get_rect().center)
        play_button_rect = play_button.get_rect(
            center=menu_surf.get_rect().center)
        if play_button_rect.collidepoint(mouse_x, mouse_y):
            jitter = (randint(-1, 1), randint(-1, 1))
            play_button_center = (menu_surf.get_rect().center[0] + jitter[0],
                                  menu_surf.get_rect().center[1] + jitter[1])
            play_button_rect = play_button.get_rect(
                center=play_button_center)
        menu_surf.blit(play_button, play_button_rect)

        quit_button_surf = game.assets.quit
        center = menu_surf.get_rect().center
        center = center[0], center[1] + 200
        quit_button_rect = quit_button_surf.get_rect(center=center)
        menu_surf.blit(quit_button_surf, quit_button_rect)

        ultrapy_surf = game.assets.ultrapy
        ultrapy_rect = ultrapy_surf.get_rect()
        ultrapy_rect.centerx = play_button_rect.centerx
        ultrapy_rect.bottom = play_button_rect.top - 20
        menu_surf.blit(ultrapy_surf, ultrapy_rect)

        blackbox_surf = game.assets.blackbox_small
        blackbox_rect = blackbox_surf.get_rect()
        blackbox_rect.centerx += 5
        menu_surf.blit(blackbox_surf, blackbox_rect)

        text_surface = game.fonts.font45.render(
            f'FPS: {game.clock.get_fps():.2f}', False, (255, 255, 255))
        text_surface2 = game.fonts.font30.render(
            'Version 0.01', False, (255, 255, 255))
        menu_surf.blit(text_surface2, (40, 45))
        menu_surf.blit(text_surface, (40, 67))

        return menu_surf, play_button_rect, quit_button_rect

    def draw(self, game):
        menu_surf, play_rect, quit_rect = self.create_menu_surface(game)
        game.screen.blit(menu_surf, (0, 0))
        return play_rect, quit_rect

    def update(self, game):
        game.pipelines.pipeline_drawing(game)
        play_rect, quit_rect = self.draw(game)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_buttons[0]:  # Check if left mouse button is down
            if play_rect.collidepoint(mouse_x, mouse_y):
                game.state = playMenu()
                logging.info(f"Changing game.state to {game.state.id}")
            elif quit_rect.collidepoint(mouse_x, mouse_y):
                quit()


class playMenu(Menu):
    def __init__(self):
        self.submenu = 0
        self.id = "Play Menu"

    def create_menu_surface(self, game):
        menu_surf = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        base_center = menu_surf.get_rect().center

        # Prelude
        prelude_button = game.assets.prelude
        prelude_center = (base_center[0] - 600, base_center[1] - 400)
        prelude_button_rect = prelude_button.get_rect(center=prelude_center)
        if prelude_button_rect.collidepoint(mouse_x, mouse_y):
            jitter = (randint(-1, 1), randint(-1, 1))
            prelude_center = (prelude_center[0] + jitter[0],
                              prelude_center[1] + jitter[1])
            prelude_button_rect = prelude_button.get_rect(
                center=prelude_center)
        menu_surf.blit(prelude_button, prelude_button_rect)

        # Act 1
        act1_button = game.assets.act1
        act1_center = (base_center[0] - 600, base_center[1] - 100)
        act1_button_rect = act1_button.get_rect(center=act1_center)
        if act1_button_rect.collidepoint(mouse_x, mouse_y):
            jitter = (randint(-1, 1), randint(-1, 1))
            act1_center = (act1_center[0] + jitter[0],
                           act1_center[1] + jitter[1])
            act1_button_rect = act1_button.get_rect(center=act1_center)
        menu_surf.blit(act1_button, act1_button_rect)

        return menu_surf, prelude_button_rect, act1_button_rect

    def draw(self, game):
        menu_surf, prelude_rect, act1_rect = self.create_menu_surface(game)
        game.screen.blit(menu_surf, (0, 0))
        return prelude_rect, act1_rect

    def update(self, game):
        game.pipelines.pipeline_drawing(game)
        prelude_rect, act1_rect = self.draw(game)

        mouse_buttons = pygame.mouse.get_pressed()
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if mouse_buttons[0]:
            if prelude_rect.collidepoint(mouse_x, mouse_y):
                logging.info("Prelude clicked")
                # TODO: start Prelude level
            elif act1_rect.collidepoint(mouse_x, mouse_y):
                logging.info("Act1 clicked")
                # TODO: start Act 1 level


class Game:
    def __init__(self) -> None:
        self.screen = pygame.display.set_mode(
            (pygame.display.Info().current_w, pygame.display.Info().current_h),
            pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.inlevel = False
        self.menu = False
        self.initalised = False

        pygame.display.set_caption("Pygame Boilerplate")

        return

    def main(self) -> int:
        for event in pygame.event.get():
            self.events.handle(self, event)

        self.state.update(self)

        pygame.display.flip()
        self.clock.tick(TICK_SPEED)

        return 0

    def quit(self):
        pygame.quit()
        sys.exit()

        return


def main() -> int:
    game.events = EventHandler()
    game.sounds = Sounds()
    game.fonts = Fonts()

    loading_surf = game.fonts.fontTitle.render(
        "LOADING", True, (255, 255, 255))
    loading_rect = loading_surf.get_rect(center=game.screen.get_rect().center)

    game.screen.blit(loading_surf, loading_rect)
    pygame.display.flip()

    game.assets = Assets()
    game.pipelines = PipelineBackground(game)

    if game.sounds.sound_working:
        pygame.mixer.music.play(-1)
    while game.running:
        game.main()

    return 0


try:
    pygame.mixer.init()
except Exception:
    sounds = False

game = Game()
game.state = mainMenu()

if __name__ == "__main__":
    result = main()

if result == 0:
    print("Exiting gracefully..")
else:
    print("Exiting with errors..")

game.quit()
