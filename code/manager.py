import pygame
from settings import *


def put_text(screen, text, color, pos_x, pos_y):
    font = pygame.font.Font(UI_FONT, 10)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos_x, pos_y)
    background = pygame.image.load("../graphics/cutscene/initial_background.png")
    screen.blit(background, [0, 100])
    screen.blit(text_surface, text_rect)


class Manager:
    def __init__(self, window):
        self.cutscene = None
        self.cutscene_is_running = False

        self.window = window
        self.window_height = 0

    def cutscene_start(self, cutscene):
        self.cutscene = cutscene
        self.cutscene_is_running = True

    def cutscene_end(self):
        self.cutscene = None
        self.cutscene_is_running = False

    def update(self):
        if self.cutscene_is_running:
            if self.window_height < self.window.get_height() * 0.3:
                self.window_height += 3
            self.cutscene_is_running = self.cutscene.update()
        else:
            self.cutscene_end()

    def draw(self):
        if self.cutscene_is_running:
            pygame.draw.rect(
                self.window,
                (0, 0, 0),
                (0, 0, self.window.get_width(), self.window_height),
            )

            self.cutscene.draw_text(self.window)
