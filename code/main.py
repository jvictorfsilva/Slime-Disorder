import sys
from menus import *
import pygame
from level import Level
from settings import *
from cutscene import Cutscene
from manager import Manager
from cutscene_dict import *

# from debug import debug
from player import *


class Game:
    def __init__(self):
        # setup geral
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.screen = screen
        pygame.display.set_caption("Slime Disorder")
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.menus = Menus()
        # sound
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.35)
        main_sound.play(loops=-1)
        self.manager = Manager(self.screen)
        self.cut = Cutscene(cutscene, 9)

    def run(self):
        menu = True
        cutscene_is_running = 0
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
                        cutscene_is_running = False
                        self.menus.pause_menu(menu)
                    if event.key == pygame.K_SPACE:
                        cutscene_is_running += 1

            self.screen.fill(WATER_COLOR)
            if cutscene_is_running <= 9:
                self.main_cutscene()
            else:
                self.level.run()

            # debug(Player.rect)
            pygame.display.update()
            self.clock.tick(FPS)

    def main_cutscene(self):
        self.manager.cutscene_start(self.cut)
        self.manager.draw()
        self.manager.update()


if __name__ == "__main__":
    game = Game()
    game.run()
