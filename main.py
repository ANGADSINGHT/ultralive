import sys
import pygame

from enum import Enum, auto

pygame.init()
sounds = True

class PipelineBackground:
    def __init__(self, game) -> None:
        self.speed = 100
        self.pipeline = game.assets.pipeline
        self.pipeline2 = game.assets.pipeline2

        self.pipeline_y = 0
        self.pipeline2_y = 1080

    def pipeline_drawing(self, game) -> int:
        self.pipeline_y += self.speed
        self.pipeline2_y += self.speed

        if self.pipeline_y >= 1080:
            self.pipeline_y = -1080
        if self.pipeline2_y >= 1080:
            self.pipeline2_y = -1080

        game.screen.blit(self.pipeline, (0, self.pipeline_y))
        game.screen.blit(self.pipeline2, (0, self.pipeline2_y))
        return 0

class GameStates(Enum):
    mainMenu = auto()

class Assets:
    def __init__(self) -> None:
        self.pipeline = pygame.image.load("assets/backgrounds/pipeline.png")
        self.pipeline2 = pygame.image.load("assets/backgrounds/pipeline2.png")
        self.play = pygame.image.load("assets/buttons/play.png")
        self.quit = pygame.image.load("assets/buttons/quit.png")
        self.ultrapy = pygame.image.load("assets/text/ultrapy.png")

class Fonts:
    def __init__(self) -> None:
        self.fontBold = pygame.font.SysFont('fonts/ultrafont.ttf', 100, bold=True)
        self.fontTitle = pygame.font.SysFont('fonts/ultrafont.ttf', 100)
        self.font20 = pygame.font.SysFont('fonts/ultrafont.ttf', 20)

class Sounds:
    def __init__(self) -> None:
        pygame.mixer.music.load("sounds/mainmenu.ogg")
        self.slam = pygame.mixer.Sound("sounds/slam.mp3")
        self.dash = pygame.mixer.Sound("sounds/dash.mp3")
        self.jump = pygame.mixer.Sound("sounds/jump.mp3")
        
        return

class KeyEventHandler:
    def __init__(self) -> None:
        return

    def handle(self, game, event) -> int:
        if event.key == pygame.K_ESCAPE:
            game.menu = not game.menu

        if game.inlevel:
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

    def create_menu_surface(self, game):
        menu_surf = pygame.Surface(game.screen.get_size(), pygame.SRCALPHA)

        play_button_surf = game.assets.play
        play_button_rect = play_button_surf.get_rect(center=menu_surf.get_rect().center)
        menu_surf.blit(play_button_surf, play_button_rect)

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

        return menu_surf, play_button_rect, quit_button_rect


    def draw(self, game):
        menu_surf, play_rect, quit_rect = self.create_menu_surface(game)
        game.screen.blit(menu_surf, (0, 0))
        
    def update(self, game):
        game.pipelines.pipeline_drawing(game)
        self.draw(game)

class Game:
    def __init__(self, sounds) -> None:
        self.screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.running = True
        self.sounds = sounds
        self.inlevel = False
        self.menu = False
        self.initalised = False
        self.gamestate = None

        pygame.display.set_caption("Pygame Boilerplate")

        return

    def main(self) -> int:
        for event in pygame.event.get():
            self.events.handle(self, event)

        match self.state:
            case GameStates.mainMenu:
                if self.gamestate is not GameStates.mainMenu:
                    self.gamestate = mainMenu()
                self.gamestate.update(self)

        pygame.display.flip()
        self.clock.tick(75)

        return 0


    def quit(self):
        pygame.quit()
        sys.exit()

        return

def main() -> int:
    game.events = EventHandler()
    game.sounds = Sounds()
    game.fonts = Fonts()
    game.assets = Assets()
    game.pipelines = PipelineBackground(game)

    loading_surf = game.fonts.fontTitle.render("LOADING", True, (255, 255, 255))
    loading_rect = loading_surf.get_rect(center=game.screen.get_rect().center)

    game.screen.blit(loading_surf, loading_rect)
    pygame.display.flip()
    pygame.time.delay(1000)


    pygame.mixer.music.play(-1)
    while game.running:
        game.state = GameStates.mainMenu
        game.main()

    return 0

try:
    pygame.mixer.init()
except Exception:
    sounds = False

game = Game(sounds)
if __name__ == "__main__":
    result = main()

if result == 0:
    print("Exiting gracefully..")
else:
    print("Exiting with errors..")

game.quit()