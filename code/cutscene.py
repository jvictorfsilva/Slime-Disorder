import pygame
from manager import put_text


class Cutscene:
    def __init__(self, dialogs, fala_final):
        self.color = (255, 255, 255)
        self.pos_x = 50
        self.pos_y = 50

        self.final_speech = fala_final
        self.step = 0
        self.speechs = dialogs

        self.speech_speed = 0.5
        self.initial_speech = 0
        self.number_speech = self.speechs[self.step]

        self.cutscene_running = True

    def update(self):
        press = pygame.key.get_pressed()
        space = press[pygame.K_SPACE]

        if self.step < self.final_speech:
            if int(self.initial_speech) < len(self.number_speech):
                self.initial_speech += self.speech_speed
            else:
                if space:
                    self.step += 1
                    self.initial_speech = 0
                    self.number_speech = self.speechs[self.step]

        elif self.step == self.final_speech:
            if int(self.initial_speech) < len(self.number_speech):
                self.initial_speech += self.speech_speed
            else:
                if space:
                    self.initial_speech = 0
                    self.cutscene_running = False

        return self.cutscene_running

    def draw_text(self, janela):
        text = self.number_speech

        put_text(
            janela,
            text[0 : int(self.initial_speech)],
            self.color,
            self.pos_x,
            self.pos_y,
        )
