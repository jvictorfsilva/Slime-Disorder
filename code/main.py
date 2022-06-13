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
        # main_sound = pygame.mixer.Sound("../audio/main.ogg")
        # main_sound.set_volume(0.2)
        # main_sound.play(loops=-1)

    def run(self):
        play_btn_image = "../graphics/buttons/play.png"
        exit_btn_image = "../graphics/buttons/exit.png"
        count = 0
        pygame.mouse.set_visible(1)

        pause_menu = False
        menu = True
        play_btn = Botao(480, 325, play_btn_image)
        exit_btn = Botao(480, 475, exit_btn_image)
        cursor = Cursor([0, 0])
        botoes = []
        botoes.append(play_btn)
        botoes.append(exit_btn)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.level.toggle_upgrade_menu()
                    if event.key == pygame.K_ESCAPE:
                        pause_menu = True

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
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_p:
                            menu = False
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if pygame.sprite.spritecollide(cursor, [play_btn], False):
                            menu = False
                        if pygame.sprite.spritecollide(cursor, [exit_btn], False):
                            pygame.quit()
                            sys.exit()
                        
                            

                cursor.rect.x = pos[0]
                cursor.rect.y = pos[1]
                self.screen.blit(cursor.image, pos)
                pygame.display.flip()

            while pause_menu == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pause_menu == True
                resume_btn_image = "../graphics/buttons/resume.png"
                exit_btn_image = "../graphics/buttons/exit.png"
                pygame.mouse.set_visible(False)

                p1 = Botao(480, 325, resume_btn_image)
                ex = Botao(480, 475, exit_btn_image)
                cursor = Cursor([0, 0])
                botoes = []
                botoes.append(p1)
                botoes.append(ex)     

                bg = pygame.image.load("../graphics/buttons/pause_menu.jpg")
                self.screen.blit(bg, [0, 0])

                logo = pygame.image.load("../graphics/buttons/logo.png")
                self.screen.blit(logo, [185, 0])

                pos = pygame.mouse.get_pos()

                for botao in botoes:
                    if botao.angulo > 0:
                        botao.angulo -= 1
                        botao.inclina()

                    self.screen.blit(botao.image, [botao.pos_x, botao.pos_y])
                    if pygame.sprite.spritecollide(cursor, [botao], False):
                        botao.angulo = 3
                        botao.inclina()

                for event in pygame.event.get():  # Verifica eventos do teclado, mouse etc
                    if event.type == pygame.QUIT:
                        pygame.quit()

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

        # Cursor = [ Cursor for Cursor in Cursor ]

if __name__ == "__main__":
    game = Game()
    game.run()