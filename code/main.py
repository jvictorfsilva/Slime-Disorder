import os, sys
from menus import *
import pygame
from level import Level
from settings import *

# from debug import debug
from player import *

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


class Game:
    def __init__(self):
        # setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Slime Disorder")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menus = Menus()
        # sound
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.05)
        main_sound.play(loops=-1)

    def run(self):
        menu = True
        if menu == True:
            self.menus.menu()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.level.toggle_upgrade_menu()
                    if event.key == pygame.K_ESCAPE:
                        self.menus.pause_menu(menu)

            self.screen.fill(WATER_COLOR)
            self.level.run()
            # debug(Player.rect)
            pygame.display.update()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()
