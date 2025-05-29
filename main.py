import pygame
import sys
from como_jogar import como_jogar

pygame.init()

largura_tela = 800
altura_tela = 800

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Flappy Bird")

fundo = pygame.image.load("imagens/inicial.png")
fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 120, 215)

fonte_titulo = pygame.font.Font('fonte/pressstart.ttf', 54)
fonte_botao = pygame.font.SysFont('Vergana', 36)

def desenhar_botao(texto, x, y, largura, altura):
    retangulo = pygame.Rect(x, y, largura, altura)
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()

    mouse_em_cima = retangulo.collidepoint(mouse)

    cor = AZUL if mouse_em_cima else BRANCO

    pygame.draw.rect(tela, cor, retangulo)

    texto_render = fonte_botao.render(texto, True, PRETO)

    texto_rect = texto_render.get_rect(center=retangulo.center)
    tela.blit(texto_render, texto_rect)
    return mouse_em_cima and clique[0]

def tela_inicial():
    while True:
        tela.blit(fundo, (0, 0))

        titulo = fonte_titulo.render("Flappy Bird", True, PRETO)
        tela.blit(titulo, (largura_tela // 2 - titulo.get_width() // 2, 100))

        if desenhar_botao("Jogar", 300, 250, 200, 60):
            print("Iniciar jogo")

        if desenhar_botao("Como jogar", 300, 350, 200,60):
            como_jogar(tela,largura_tela,altura_tela)

        if desenhar_botao("Sair", 300, 650, 200, 60):
            pygame.quit()
            sys.exit()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

tela_inicial()
