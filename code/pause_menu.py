import pygame
from settings import *


class Pause_menu:
    def __init__(self):

        # general setup
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

    def menu_interface(self):
        resume_btn_image = "../graphics/buttons/resume.png"
        options_btn_image = "../graphics/buttons/options.png"
        exit_btn_image = "../graphics/buttons/exit.png"
        count = 0
        pygame.mouse.set_visible(False)

        pos = pygame.mouse.get_pos()

        bg = pygame.image.load("../graphics/buttons/pause_menu.png")
        self.screen.blit(bg, [0, 0])

        logo = pygame.image.load("../graphics/buttons/logo.png")
        self.screen.blit(logo, [185, 0])

        p1 = Botao(480, 280, resume_btn_image)
        p2 = Botao(480, 425, options_btn_image)
        ex = Botao(480, 570, exit_btn_image)
        cursor = Cursor([0, 0])
        botoes = []
        botoes.append(p1)
        botoes.append(p2)
        botoes.append(ex)

        count += 1

        for botao in botoes:
            if botao.angulo > 0:
                botao.angulo -= 1
                botao.inclina()

            self.screen.blit(botao.image, [botao.pos_x, botao.pos_y])
            if pygame.sprite.spritecollide(cursor, [botao], False):
                botao.angulo = 3
                botao.inclina()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        cursor.rect.x = pos[0]
        cursor.rect.y = pos[1]
        self.screen.blit(cursor.image, pos)
        pygame.display.flip()

    def display(self):
        self.menu_interface()


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
