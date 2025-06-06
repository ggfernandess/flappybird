import pygame
import sys
import os
import math
from random import randint
from pygame import Rect
from pygame.locals import *

# --- Configurações iniciais ---
pygame.init()
FPS = 60

largura_tela = 800
altura_tela = 800

tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Flappy Bird")

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 120, 215)
AZUL_CEU = (135, 206, 235)

fonte_titulo = pygame.font.SysFont('Arial', 54, bold=True)
fonte_botao = pygame.font.SysFont('Verdana', 36)
fonte_pontuacao = pygame.font.SysFont('Arial', 48, bold=True)

# --- Funções auxiliares ---
def load_image(img_file_name):
    try:
        base_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_path, 'images', img_file_name)
        img = pygame.image.load(path).convert_alpha()
        return img
    except:
        print(f"Imagem não encontrada: {img_file_name}, criando placeholder")
        if 'bird' in img_file_name:
            surf = pygame.Surface((32, 32), SRCALPHA)
            pygame.draw.circle(surf, (255, 255, 0), (16, 16), 15)
            return surf
        elif 'pipe' in img_file_name:
            surf = pygame.Surface((80, 32), SRCALPHA)
            pygame.draw.rect(surf, (0, 255, 0), (0, 0, 80, 32))
            return surf
        else:
            surf = pygame.Surface((largura_tela, altura_tela))
            surf.fill(AZUL_CEU)
            return surf

def load_images():
    return {
        'background': load_image('inicial.png'),
        'pipe-end': load_image('pipe_end.png'),
        'pipe-body': load_image('pipe_body.png'),
        'bird-wingup': load_image('bird_wing_up.png'),
        'bird-wingdown': load_image('bird_wing_down.png')
    }

def desenhar_botao(texto, x, y, largura, altura):
    retangulo = pygame.Rect(x, y, largura, altura)
    mouse = pygame.mouse.get_pos()
    clique = pygame.mouse.get_pressed()
    mouse_em_cima = retangulo.collidepoint(mouse)
    cor = AZUL if mouse_em_cima else BRANCO
    pygame.draw.rect(tela, cor, retangulo)
    pygame.draw.rect(tela, PRETO, retangulo, 2)
    texto_render = fonte_botao.render(texto, True, PRETO)
    texto_rect = texto_render.get_rect(center=retangulo.center)
    tela.blit(texto_render, texto_rect)
    return mouse_em_cima and clique[0]

# --- Classes ---
class Bird(pygame.sprite.Sprite):
    WIDTH = HEIGHT = 32
    SINK_SPEED = 0.3       # cai mais rápido
    CLIMB_SPEED = 0.28     # sobe rápido
    CLIMB_DURATION = 300   # duração do pulo em ms

    def __init__(self, x, y, msec_to_climb, images):
        super(Bird, self).__init__()
        self.x, self.y = x, y
        self.msec_to_climb = msec_to_climb
        self._img_wingup, self._img_wingdown = images
        self._mask_wingup = pygame.mask.from_surface(self._img_wingup)
        self._mask_wingdown = pygame.mask.from_surface(self._img_wingdown)

    def update(self, delta_ms):
        if self.msec_to_climb > 0:
            frac_climb_done = 1 - self.msec_to_climb / Bird.CLIMB_DURATION
            deslocamento = Bird.CLIMB_SPEED * delta_ms * (1 - math.cos(frac_climb_done * math.pi))
            self.y -= deslocamento
            self.msec_to_climb -= delta_ms
            if self.msec_to_climb < 0:
                self.msec_to_climb = 0
        else:
            self.y += Bird.SINK_SPEED * delta_ms

    @property
    def image(self):
        return self._img_wingup if pygame.time.get_ticks() % 500 >= 250 else self._img_wingdown

    @property
    def mask(self):
        return self._mask_wingup if pygame.time.get_ticks() % 500 >= 250 else self._mask_wingdown

    @property
    def rect(self):
        return Rect(self.x, self.y, Bird.WIDTH, Bird.HEIGHT)

class PipePair(pygame.sprite.Sprite):
    WIDTH = 80
    PIECE_HEIGHT = 32
    ADD_INTERVAL = 3000
    SPEED = 0.15  # velocidade do cano

    def __init__(self, pipe_end_img, pipe_body_img):
        super(PipePair, self).__init__()
        self.x = float(largura_tela)
        self.score_counted = False
        self.pipe_end_img = pipe_end_img
        self.pipe_body_img = pipe_body_img

        gap_size = 5 * Bird.HEIGHT
        max_pipe_height = altura_tela - gap_size - 2 * PipePair.PIECE_HEIGHT

        self.bottom_pieces = randint(1, max_pipe_height // PipePair.PIECE_HEIGHT)
        self.top_pieces = (max_pipe_height // PipePair.PIECE_HEIGHT) - self.bottom_pieces

        total_height = altura_tela
        self.image = pygame.Surface((PipePair.WIDTH, total_height), SRCALPHA)
        self.image.fill((0, 0, 0, 0))

        # Retângulos para colisão das partes do cano
        self.rects = []

        # Cano inferior - corpo
        bottom_start_y = altura_tela - self.bottom_pieces * PipePair.PIECE_HEIGHT
        for i in range(self.bottom_pieces):
            y = bottom_start_y + i * PipePair.PIECE_HEIGHT
            self.image.blit(self.pipe_body_img, (0, y))
            self.rects.append(pygame.Rect(0, y, PipePair.WIDTH, PipePair.PIECE_HEIGHT))
        # Cano inferior - pipe end
        self.image.blit(self.pipe_end_img, (0, bottom_start_y - PipePair.PIECE_HEIGHT))
        self.rects.append(pygame.Rect(0, bottom_start_y - PipePair.PIECE_HEIGHT, PipePair.WIDTH, PipePair.PIECE_HEIGHT))

        # Cano superior - corpo
        for i in range(self.top_pieces):
            y = i * PipePair.PIECE_HEIGHT
            self.image.blit(self.pipe_body_img, (0, y))
            self.rects.append(pygame.Rect(0, y, PipePair.WIDTH, PipePair.PIECE_HEIGHT))
        # Cano superior - pipe end invertido
        pipe_end_upside_down = pygame.transform.flip(self.pipe_end_img, False, True)
        self.image.blit(pipe_end_upside_down, (0, self.top_pieces * PipePair.PIECE_HEIGHT))
        self.rects.append(pygame.Rect(0, self.top_pieces * PipePair.PIECE_HEIGHT, PipePair.WIDTH, PipePair.PIECE_HEIGHT))

    @property
    def rect(self):
        return Rect(self.x, 0, PipePair.WIDTH, altura_tela)

    def update(self, delta_ms):
        self.x -= PipePair.SPEED * delta_ms

    def colisao_com_bird(self, bird_rect):
        for rect in self.rects:
            rect_move = rect.move(self.x, 0)
            if rect_move.colliderect(bird_rect):
                return True
        return False

# --- Função do menu inicial ---
def menu_inicial(images):
    relogio = pygame.time.Clock()
    rodando = True

    while rodando:
        tela.blit(images['background'], (0, 0))
        titulo = fonte_titulo.render("FLAPPY BIRD", True, PRETO)
        tela.blit(titulo, titulo.get_rect(center=(largura_tela//2, 150)))

        jogar_clicado = desenhar_botao("Jogar", largura_tela//2 - 100, 300, 200, 60)
        como_jogar_clicado = desenhar_botao("Como Jogar", largura_tela//2 - 140, 400, 280, 60)
        sair_clicado = desenhar_botao("Sair", largura_tela//2 - 100, 500, 200, 60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar_clicado:
            return 'jogar'
        if como_jogar_clicado:
            return 'como_jogar'
        if sair_clicado:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        relogio.tick(FPS)

# --- Função do menu como jogar ---
def menu_como_jogar(tela, largura_tela, altura_tela):
    base_path = os.path.dirname(os.path.abspath(__file__))
    fonte_path = os.path.join(base_path, 'pressstart.ttf')
    fonte_texto = pygame.font.Font(fonte_path, 25) if os.path.exists(fonte_path) else pygame.font.SysFont('Arial', 25)

    img_path = os.path.join(base_path, 'images', 'comojogar.webp')
    if os.path.exists(img_path):
        fundo = pygame.image.load(img_path).convert_alpha()
        fundo = pygame.transform.scale(fundo, (largura_tela, altura_tela))
        fundo.set_alpha(40)
    else:
        fundo = pygame.Surface((largura_tela, altura_tela))
        fundo.fill(AZUL_CEU)
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

# --- Função principal do jogo ---
def jogar(images):
    relogio = pygame.time.Clock()

    bird = Bird(200, altura_tela//2, 0, (images['bird-wingup'], images['bird-wingdown']))
    pipes = []
    tempo_ultimo_cano = 0

    pontuacao = 0
    rodando = True

    while rodando:
        delta_ms = relogio.tick(FPS)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    bird.msec_to_climb = Bird.CLIMB_DURATION

        # Atualiza o pássaro
        bird.update(delta_ms)

        # Cria novos canos periodicamente
        tempo_ultimo_cano += delta_ms
        if tempo_ultimo_cano > PipePair.ADD_INTERVAL:
            pipes.append(PipePair(images['pipe-end'], images['pipe-body']))
            tempo_ultimo_cano = 0

        # Atualiza canos e remove os que saíram da tela
        for pipe in pipes[:]:
            pipe.update(delta_ms)
            if pipe.x < -PipePair.WIDTH:
                pipes.remove(pipe)

        # Verifica colisões
        bird_rect = bird.rect

        for pipe in pipes:
            if pipe.colisao_com_bird(bird_rect):
                rodando = False  # bateu, fim de jogo

            # Pontuação: conta se passar pelo cano
            if not pipe.score_counted and pipe.x + PipePair.WIDTH < bird.x:
                pontuacao += 1
                pipe.score_counted = True

        # Verifica se o pássaro bateu no chão ou no teto
        if bird.y > altura_tela - Bird.HEIGHT or bird.y < 0:
            rodando = False

        # Desenha tudo
        tela.blit(images['background'], (0, 0))

        for pipe in pipes:
            tela.blit(pipe.image, (pipe.x, 0))

        tela.blit(bird.image, (bird.x, bird.y))

        # Desenha pontuação atual
        pontuacao_render = fonte_pontuacao.render(str(pontuacao), True, PRETO)
        tela.blit(pontuacao_render, pontuacao_render.get_rect(center=(largura_tela // 2, 50)))

        pygame.display.update()

    return pontuacao

# --- Função para mostrar pontuação final ---
def tela_game_over(pontuacao, background):
    relogio = pygame.time.Clock()
    run = True

    while run:
        tela.blit(background, (0, 0))  # desenha o background

        texto_game_over = fonte_titulo.render("Game Over", True, PRETO)
        texto_pontuacao = fonte_botao.render(f"Sua pontuação: {pontuacao}", True, PRETO)

        tela.blit(texto_game_over, texto_game_over.get_rect(center=(largura_tela // 2, 150)))
        tela.blit(texto_pontuacao, texto_pontuacao.get_rect(center=(largura_tela // 2, 250)))

        jogar_novamente = desenhar_botao("Jogar Novamente", largura_tela // 2 - 150, 350, 300, 60)
        sair = desenhar_botao("Sair", largura_tela // 2 - 100, 450, 200, 60)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if jogar_novamente:
            run = False
            return True
        if sair:
            pygame.quit()
            sys.exit()

        pygame.display.update()
        relogio.tick(FPS)

# --- Loop principal do programa ---
def main():
    imagens = load_images()

    while True:
        acao = menu_inicial(imagens)

        if acao == 'jogar':
            pontuacao = jogar(imagens)
            jogar_novamente = tela_game_over(pontuacao, imagens['background'])
            if not jogar_novamente:
                break
        elif acao == 'como_jogar':
            menu_como_jogar(tela, largura_tela, altura_tela)

if __name__ == "__main__":
    main()
