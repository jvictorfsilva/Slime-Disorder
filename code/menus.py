import pygame
import sys
from settings import *


class Menus:
    def __init__(self):
        self.main_menu = True
        self.pause = False
        self.display_surface = pygame.display.get_surface()
        # self.pos = pygame.mouse.get_pos()

    def menu(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        cursor = Cursor([0, 0])
        play_btn_image = "../graphics/buttons/play.png"
        exit_btn_image = "../graphics/buttons/exit.png"
        play_btn = Botao(480, 325, play_btn_image)
        exit_btn = Botao(480, 475, exit_btn_image)
        botoes = []
        while self.main_menu == True:

            botoes.append(play_btn)
            botoes.append(exit_btn)
            pos = pygame.mouse.get_pos()

            bg = pygame.image.load("../graphics/buttons/main_menu.jpg")
            self.screen.blit(bg, [0, 0])

            for botao in botoes:
                self.screen.blit(botao.image, [botao.pos_x, botao.pos_y])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pygame.sprite.spritecollide(cursor, [play_btn], False):
                        self.main_menu = False
                    if pygame.sprite.spritecollide(cursor, [exit_btn], False):
                        pygame.quit()
                        sys.exit()

            cursor.rect.x = pos[0]
            cursor.rect.y = pos[1]
            self.screen.blit(cursor.image, pos)
            pygame.display.flip()

    def pause_menu(self, menu):
        self.pause = True
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        while self.pause == True:

            bg = pygame.image.load("../graphics/buttons/pause_menu.png")
            self.screen.blit(bg, [0, 0])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False

            pygame.display.flip()


class Botao(pygame.sprite.Sprite):
    def __init__(self, x, y, image):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.original = pygame.image.load(image)
        self.angle = 0
        self.rect = self.image.get_rect()
        self.pos_x = x
        self.pos_y = y

        self.rect.x = x
        self.rect.y = y

    def __str__(self):
        return self.name


class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.mouse.set_visible(False)
        cursor_img = "../graphics/buttons/cursor.png"
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(cursor_img)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.selec = 1
