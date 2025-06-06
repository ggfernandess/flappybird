import pygame
import sys
import os

pygame.init()

# CORES
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

def como_jogar(tela, largura_tela, altura_tela):
    base_path = os.path.dirname(os.path.abspath(__file__))  # pasta do script atual

    # Caminho absoluto da fonte
    fonte_path = os.path.join(base_path, 'pressstart.ttf')
    fonte_texto = pygame.font.Font(fonte_path, 25)

    # Caminho absoluto da imagem de fundo
    img_path = os.path.join(base_path, 'images', 'comojogar.webp')
    fundo = pygame.image.load(img_path).convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))
    fundo.set_alpha(40)

    clock = pygame.time.Clock()

    texto = [
        "Como Jogar:",
        "- Use espaço para pular",
        "- Evite os obstáculos",
        "- Pontue o máximo possível",
        "",
        "Pressione ESC para voltar"
    ]

    run = True
    while run:
        tela.blit(fundo, (0, 0))

        y = 250
        espaco = 40

        for linha in texto:
            render = fonte_texto.render(linha, True, PRETO)
            tela.blit(render, (50, y))
            y += espaco

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    run = False

        pygame.display.update()
        clock.tick(60)
