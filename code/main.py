import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)


import pygame
from level import Level
from settings import *

# from debug import debug


class Game:
    def __init__(self):
        # setup geral
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Slime Disorder")
        self.clock = pygame.time.Clock()

        self.level = Level()

        # sound
        main_sound = pygame.mixer.Sound("../audio/main.ogg")
        main_sound.set_volume(0.2)
        main_sound.play(loops=-1)

    def run(self):
        play_btn_image = "../graphics/buttons/play.png"
        options_btn_image = "../graphics/buttons/options.png"
        exit_btn_image = "../graphics/buttons/exit.png"
        count = 0
        pygame.mouse.set_visible(1)

        menu = False
        p1 = Botao(480, 280, play_btn_image)
        p2 = Botao(480, 425, options_btn_image)
        ex = Botao(480, 570, exit_btn_image)
        cursor = Cursor([0, 0])
        botoes = []
        botoes.append(p1)
        botoes.append(p2)
        botoes.append(ex)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.level.toggle_upgrade_menu()
                    if event.key == pygame.K_ESCAPE:
                        self.level.toggle_pause_menu()

            count += 1

            while menu == True:
                pos = pygame.mouse.get_pos()

                bg = pygame.image.load("../graphics/buttons/main_menu.jpg")
                self.screen.blit(bg, [0, 0])

                for botao in botoes:
                    if botao.angulo > 0:
                        botao.angulo -= 1
                        botao.inclina()

                    self.screen.blit(botao.image, [botao.pos_x, botao.pos_y])
                    if pygame.sprite.spritecollide(cursor, [botao], False):
                        botao.angulo = 3
                        botao.inclina()

                for (
                    event
                ) in pygame.event.get():  # Verifica eventos do teclado, mouse etc
                    if event.type == pygame.QUIT:
                        sys.exit()

                cursor.rect.x = pos[0]
                cursor.rect.y = pos[1]
                self.screen.blit(cursor.image, pos)
                pygame.display.flip()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            # debug('Test')
            pygame.display.update()
            self.clock.tick(FPS)


class Botao(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.original = pygame.image.load(image)
        self.angulo = 0
        self.image = pygame.transform.rotate(self.original, self.angulo)
        # posicao no quadro
        self.rect = self.image.get_rect()
        # posicao relativa
        self.pos_x = x
        self.pos_y = y

        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return self.name

    def inclina(self):
        self.image = pygame.transform.rotate(self.original, self.angulo)


class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.mouse.set_visible(False)
        cursor_img = "../graphics/buttons/cursor.png"
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cursor_img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.selec = 1


if __name__ == "__main__":
    game = Game()
    game.run()
