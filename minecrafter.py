import pygame
import sys
import random

# Inicializa o Pygame
pygame.init()

# Inicializa o mixer de áudio do Pygame
pygame.mixer.init()

# Carrega a trilha sonora
pygame.mixer.music.load(r"C:\Users\nicol\Documents\Nova pasta (7)\cte\minecraft 2\Calmo e Relaxante.mp3")  # Usa string "raw" para evitar problemas com barras invertidas
pygame.mixer.music.set_volume(0.5)  # Define o volume da trilha (opcional)
pygame.mixer.music.play(-1)  # Toca a música em loop infinito (-1 para loop)
# Define cores
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)  # Cor do objetivo
BLACK = (0, 0, 0)

# Configurações da janela
WIDTH, HEIGHT = 1200, 650
BLOCK_SIZE = 40

# Inicializa a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Minecraft 2D Simples - Fases')

# Configurações do jogador
player_pos = [WIDTH // 2, 0]  # Posição inicial do jogador
player_size = 30  # Tamanho do jogador
player_color = BLACK  # Cor do jogador (preto)
player_velocity_y = 0  # Velocidade vertical do jogador
gravity = 0.5  # Gravidade
grounded = True  # Verifica se o jogador está no chão
jump_height = 12  # Altura do pulo

# Função para gerar o terreno com obstáculos
def generate_terrain():
    terrain = [[0 for _ in range(WIDTH // BLOCK_SIZE)] for _ in range(HEIGHT // BLOCK_SIZE)]
    base_height = random.randint(HEIGHT // BLOCK_SIZE // 2, HEIGHT // BLOCK_SIZE // 2 + 3)  # Varia altura de base
    for i in range(base_height, HEIGHT // BLOCK_SIZE):
        for j in range(WIDTH // BLOCK_SIZE):
            if random.random() < 0.1 and i > HEIGHT // BLOCK_SIZE // 2:  # 10% de chance de gerar blocos aleatórios
                terrain[i][j] = 1  # Bloco de obstáculo
            elif i >= base_height:
                terrain[i][j] = 1  # Cria o terreno base

    # Adiciona montanhas aleatórias
    for _ in range(random.randint(3, 7)):  # Gera de 3 a 7 montanhas
        mountain_height = random.randint(3, 6)
        mountain_width = random.randint(3, 6)
        x_start = random.randint(0, WIDTH // BLOCK_SIZE - mountain_width)
        y_start = base_height - mountain_height

        for i in range(y_start, y_start + mountain_height):
            for j in range(x_start, x_start + mountain_width):
                if 0 <= i < HEIGHT // BLOCK_SIZE and 0 <= j < WIDTH // BLOCK_SIZE:
                    terrain[i][j] = 1
    return terrain

# Gera o terreno inicial
terrain = generate_terrain()

# Gera o quadrado amarelo (objetivo) em uma posição aleatória acima do terreno
def generate_goal():
    while True:
        x = random.randint(0, WIDTH // BLOCK_SIZE - 1)
        y = random.randint(0, HEIGHT // BLOCK_SIZE // 2 - 3)  # Gera longe do terreno
        if terrain[y][x] == 0:  # Garante que não gera no bloco
            return [x * BLOCK_SIZE, y * BLOCK_SIZE]

goal_pos = generate_goal()

# Função para desenhar os blocos
def draw_blocks():
    for i, row in enumerate(terrain):
        for j, block in enumerate(row):
            if block == 1:
                pygame.draw.rect(screen, BROWN, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Função para desenhar o jogador
def draw_player():
    pygame.draw.rect(screen, player_color, (player_pos[0], player_pos[1], player_size, player_size))

# Função para desenhar o objetivo (quadrado amarelo)
def draw_goal():
    pygame.draw.rect(screen, YELLOW, (*goal_pos, BLOCK_SIZE, BLOCK_SIZE))

# Função para desenhar o degradê no fundo com cores dinâmicas
def draw_gradient(gradient_colors):
    for i in range(HEIGHT):
        # Define uma cor de degradê variando entre os valores fornecidos
        color = (
            int(gradient_colors[0][0] + (gradient_colors[1][0] - gradient_colors[0][0]) * (i / HEIGHT)),
            int(gradient_colors[0][1] + (gradient_colors[1][1] - gradient_colors[0][1]) * (i / HEIGHT)),
            int(gradient_colors[0][2] + (gradient_colors[1][2] - gradient_colors[0][2]) * (i / HEIGHT))
        )
        pygame.draw.line(screen, color, (0, i), (WIDTH, i))

# Função para desenhar a lua em uma posição aleatória
def draw_moon(moon_pos):
    moon_radius = 50
    pygame.draw.circle(screen, WHITE, moon_pos, moon_radius)
    pygame.draw.circle(screen, (200, 200, 200), (moon_pos[0] + 20, moon_pos[1] - 10), moon_radius - 10)  # Sombra na lua

# Função para verificar colisões com o terreno
def check_collision():
    global grounded, player_velocity_y
    grounded = False
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)

    for i, row in enumerate(terrain):
        for j, block in enumerate(row):
            if block == 1:
                block_rect = pygame.Rect(j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                if player_rect.colliderect(block_rect):
                    if player_velocity_y > 0:  # Se o jogador está caindo
                        player_pos[1] = block_rect.top - player_size  # Pousar em cima do bloco
                        grounded = True
                        return

# Função para verificar se o jogador está colidindo com o objetivo (quadrado amarelo)
def check_goal_collision():
    player_rect = pygame.Rect(player_pos[0], player_pos[1], player_size, player_size)
    goal_rect = pygame.Rect(goal_pos[0], goal_pos[1], BLOCK_SIZE, BLOCK_SIZE)
    if player_rect.colliderect(goal_rect):
        return True
    return False

# Reinicia a fase (novo terreno, objetivo, lua e degradê)
def next_phase():
    global terrain, goal_pos, player_pos, player_velocity_y, moon_pos, gradient_colors
    terrain = generate_terrain()
    goal_pos = generate_goal()
    player_pos = [WIDTH // 2, 0]  # Reseta a posição do jogador
    player_velocity_y = 0  # Reseta a velocidade do jogador
    moon_pos = (random.randint(100, WIDTH - 100), random.randint(50, 200))  # Posição aleatória da lua
    gradient_colors = [(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)),
                       (random.randint(0, 150), random.randint(0, 150), random.randint(0, 150))]  # Cores aleatórias

# Configurações iniciais da lua e do degradê
moon_pos = (random.randint(100, WIDTH - 100), random.randint(50, 200))  # Posição inicial aleatória da lua
gradient_colors = [(135, 206, 235), (0, 0, 128)]  # Cores iniciais do degradê (céu claro para escuro)

# Loop principal
clock = pygame.time.Clock()
while True:
    screen.fill(WHITE)

    # Desenha o degradê e a lua no fundo
    draw_gradient(gradient_colors)
    draw_moon(moon_pos)

    # Verifica eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Colocar e destruir blocos
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            block_x, block_y = x // BLOCK_SIZE, y // BLOCK_SIZE

            if event.button == 1:  # Botão esquerdo do mouse (colocar bloco)
                if terrain[block_y][block_x] == 0:
                    terrain[block_y][block_x] = 1
            if event.button == 3:  # Botão direito do mouse (destruir bloco)
                if terrain[block_y][block_x] == 1:
                    terrain[block_y][block_x] = 0

    # Movimento do jogador
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += 5

    # Pulo
    if keys[pygame.K_SPACE] and grounded:
        player_velocity_y = -jump_height
        grounded = False

    # Aplicando gravidade
    player_velocity_y += gravity
    player_pos[1] += player_velocity_y

    # Verificar colisões
    check_collision()

    # Verificar se o jogador está colidindo com o objetivo
    if check_goal_collision():
        next_phase()  # Passa para a próxima fase quando colidir com o quadrado amarelo

    # Se o jogador está no chão, resete a velocidade vertical
    if grounded:
        player_velocity_y = 0
        if player_pos[1] > HEIGHT - player_size:
            player_pos[1] = HEIGHT - player_size

    # Verificar se o jogador está fora da tela
    if player_pos[0] < 0 or player_pos[0] > WIDTH:
        player_pos = [WIDTH // 2, 0]

    # Desenha o terreno, o jogador e o objetivo
    draw_blocks()
    draw_player()
    draw_goal()

    # Atualiza a tela
    pygame.display.flip()
    clock.tick(30)
