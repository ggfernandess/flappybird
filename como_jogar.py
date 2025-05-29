import pygame
import sys

pygame.init()

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

def como_jogar(tela, largura_tela, altura_tela):
    clock = pygame.time.Clock()
    fonte_texto = pygame.font.Font('fonte/pressstart.ttf', 25)

   
    fundo = pygame.image.load("imagens/comojogar.webp").convert_alpha()
    fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))
    fundo.set_alpha(40)  

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
