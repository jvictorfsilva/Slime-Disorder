import pygame
from settings import *

# Criar a função de colocar texto


def put_text(screen, text, color, pos_x, pos_y):
    font = pygame.font.Font(UI_FONT, 10)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (pos_x, pos_y)
    background = pygame.image.load("../graphics/cutscene/initial_background.png")
    screen.blit(background, [0, 100])
    screen.blit(text_surface, text_rect)


# Criar a classe gerenciador


class Manager:
    # Criar o método de inicialização
    def __init__(self, window):
        # Declarar as varáveis de armazenamento da cutscene
        self.cutscene = None
        self.cutscene_is_running = False

        # Declarar as variáveis dos parâmetros
        self.window = window
        self.window_height = 0

    # Criar o método start
    def cutscene_start(self, cutscene):
        # Colocar os valores dos parâmetros nas variáveis
        self.cutscene = cutscene
        self.cutscene_is_running = True

    # Criar o método end
    def cutscene_end(self):
        # Resetar os valores das variáveis
        self.cutscene = None
        self.cutscene_is_running = False

    # Criar o método update
    def update(self):
        # Checar se a cutscene está rodando ou não
        if self.cutscene_is_running:
            # Se estiver
            if self.window_height < self.window.get_height() * 0.3:
                self.window_height += 3
                # Checar se a caixa de diálogo está desenhada
            self.cutscene_is_running = self.cutscene.update()
            # Chamar o método de atualização
        else:
            # Se não
            self.cutscene_end()
            # Chamar o método End

    # Criar o método draw
    def draw(self):
        # Desenhar a caixa de diálogo
        if self.cutscene_is_running:
            pygame.draw.rect(
                self.window,
                (0, 0, 0),
                (0, 0, self.window.get_width(), self.window_height),
            )

            # Desenhar a fala da cutscene
            self.cutscene.draw_text(self.window)
