import pygame
from settings import *
from support import *
import pandas as pd


class Dialog:
    def __init__(self):
        self.font = pygame.font.Font(UI_FONT, 10)
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load("../graphics/dialog/DialogBoxFaceset.png")
        self.icon = pygame.image.load("../graphics/dialog/Facesets/Samurai.png")
        df = pd.read_csv("../dialogs/dialogs.csv", delimiter=";")
        self.i = 0
        dfstr = df["text"][self.i]

        self.text_surf = pygame.font.Font.render(
            (self.font),
            dfstr,
            True,
            "#000000",
        )
        x = 933
        y = 575
        self.text_rect = self.text_surf.get_rect(center=(x, y))

    def dialog(self):
        self.pause = True
        while self.pause == True:
            if self.i < 16:
                self.display_surface.blit(self.bg, [270, 500])
                self.display_surface.blit(self.icon, [286, 536])

            for event in pygame.event.get():  # Verifica eventos do teclado, mouse etc
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = False
                    if (
                        event.key == pygame.K_KP_ENTER
                        or event.key == pygame.K_SPACE
                        and self.i < 16
                    ):
                        self.dialog_text(self.i)
                        self.i += 1
                    elif (
                        self.i == 15
                        and event.key == pygame.K_KP_ENTER
                        or event.key == pygame.K_SPACE
                    ):
                        self.pause = False
                    else:
                        self.i = 0
        pygame.display.flip()

    def dialog_text(self, number):
        df = pd.read_csv("../dialogs/dialogs.csv", delimiter=";")
        dfstr = str(df["text"][number])
        self.dfstr_count = len(dfstr)

        self.text_surf = pygame.font.Font.render(
            (self.font),
            dfstr,
            False,
            UI_BG_COLOR,
        )
        x = 406
        y = 542
        self.text_rect = pygame.Rect((x, y), (622, 86))
        self.display_surface.blit(self.text_surf, self.text_rect)

        pygame.display.flip()
