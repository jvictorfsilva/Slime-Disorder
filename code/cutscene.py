import pygame
from manager import put_text

# Criar a classe Cutscene


class Cutscene:
    # Criar o metodo de init
    def __init__(self, dialogs, fala_final):
        # Criar as variaveis para desenhar o texto pela função
        self.color = (255, 255, 255)
        self.pos_x = 50
        self.pos_y = 50

        # Criar as variáveis de exibição de fala
        self.final_speech = fala_final
        self.step = 0
        self.speechs = dialogs

        # Criar as variáveis de controle da classe
        self.speech_speed = 0.5
        self.initial_speech = 0
        self.number_speech = self.speechs[self.step]

        # Criar a variável de retorno da atualizaçãp
        self.cutscene_running = True

    # Criar o método atuialização e suas checagens
    def update(self):
        # Colocar o evento de apertar espaço
        press = pygame.key.get_pressed()
        space = press[pygame.K_SPACE]

        # Colocar as checagens
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

        # Colocar o retorno de acordo com a variável anterior
        return self.cutscene_running

    # Criar o método de desenhar texto
    def draw_text(self, janela):
        # atribuir a variável de texto ao parâmetro texto da função
        text = self.number_speech

        # Colocar a função de desenhar o texto
        put_text(
            janela,
            text[0 : int(self.initial_speech)],
            self.color,
            self.pos_x,
            self.pos_y,
        )
