import pygame
import random

# Defina as constantes do jogo
WIDTH = 800
HEIGHT = 600
FPS = 60

# Defina as cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Inicialize o Pygame e crie a janela do jogo
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo de Avião")
clock = pygame.time.Clock()

# Carregue a imagem de fundo e redimensione-a para a tela
background = pygame.image.load('img/Небо, тучи.jpg').convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# Crie os grupos de sprites
all_sprites = pygame.sprite.Group()
missiles = pygame.sprite.Group()
bullets = pygame.sprite.Group()


# Defina as classes do jogo
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites)
        self.image = pygame.image.load(
            'img/94df9119-88c0-405e-a00b-cc26c67d9022-removebg-preview 1.png')  # carrega a imagem do jogador
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.top < 0:
            self.rect.top = 0


class Missile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(all_sprites, missiles)
        self.image = pygame.image.load('img/Design_sem_nome__1_-removebg-preview 1.png')  # carrega a imagem do míssil
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(3, 8)

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(3, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, bullets)
        self.image = pygame.image.load('img/images-removebg-preview (1) 1.png  '  ) # carrega a imagem da bala
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


# Crie o jogador e adicione-o ao grupo de jogadores
player = Player()

# Variáveis para o contador de pontos
score = 0
start_time = pygame.time.get_ticks()

# Loop principal do jogo
running = True
while running:
    # Mantenha o loop na taxa de quadros correta
    clock.tick(FPS)

    # Processa eventos (teclas, cliques, etc)
    for event in pygame.event.get():
        # Verifique seo jogador quer sair do jogo
        if event.type == pygame.QUIT:
            running = False
        # Verifique se a barra de espaço foi pressionada para atirar
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Crie uma nova bala na posição do jogador
                bullet = Bullet(player.rect.centerx, player.rect.top)

    # Gere novos mísseis aleatoriamente
    if random.randrange(100) < 2:
        Missile()

    # Atualize a posição dos sprites
    all_sprites.update()

    # Verifique a colisão entre as balas e os mísseis
    hits = pygame.sprite.groupcollide(missiles, bullets, True, True)
    # Adicione 1 ponto para cada míssil eliminado
    score += len(hits)

    # Verifique a colisão entre o jogador e os mísseis
    hits = pygame.sprite.spritecollide(player, missiles, False)
    if hits:
        running = False

    # Calcule o tempo decorrido em segundos e exiba o número de pontos na tela
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)

    # Desenhe a tela
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    screen.blit(text, (10, 10))

    # Depois de desenhar tudo, flip a tela
    pygame.display.flip()

# Desenhe a tela de "Game Over"
font = pygame.font.Font(None, 64)
text = font.render("Game Over", True, WHITE)
screen.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
pygame.display.flip()

# Espere por 3 segundos antes de encerrar o Pygame
pygame.time.wait(3000)

# Encerre o Pygame
pygame.quit()
