import pygame
import math
import sys
import os

# Configurações da tela
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHT_GRAY = (200, 200, 200)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Órbita Elíptica do Satélite")
clock = pygame.time.Clock()

# Localização do diretório onde o script está
base_dir = os.path.dirname(__file__)

# Caminhos das imagens
earth_image_path = os.path.join(base_dir, 'earth.png')
satellite_image_path = os.path.join(base_dir, 'satellite.png')

# Carregar imagens
try:
    earth_image = pygame.image.load(earth_image_path)
    earth_image = pygame.transform.scale(
        earth_image, (60, 60))  # Ajuste o tamanho da Terra
    satellite_image = pygame.image.load(satellite_image_path)
    satellite_image = pygame.transform.scale(
        satellite_image, (20, 20))  # Ajuste o tamanho do satélite
except pygame.error as e:
    print(f"Erro ao carregar imagens: {e}")
    pygame.quit()
    sys.exit()

# Parâmetros da órbita
center_x, center_y = WIDTH // 2, HEIGHT // 2  # Centro do planeta
a = 200  # Semi-eixo maior da elipse
b = 100  # Semi-eixo menor da elipse
angle = 0  # Ângulo inicial
angular_velocity = 0.01  # Velocidade angular

# Variáveis de controle
running = True
show_orbit_path = True
orbit_points = []  # Armazena os pontos da órbita para desenhar a linha
camera_offset_x = 0  # Deslocamento horizontal da câmera
camera_offset_y = 0  # Deslocamento vertical da câmera

# Função para lidar com eventos


def handle_events():
    global running, show_orbit_path, a, b, angular_velocity, camera_offset_x, camera_offset_y
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                show_orbit_path = not show_orbit_path
            elif event.key == pygame.K_UP:
                a += 10
                b += 5
            elif event.key == pygame.K_DOWN:
                a = max(50, a - 10)
                b = max(25, b - 5)
            elif event.key == pygame.K_LEFT:
                camera_offset_x -= 10  # Mover a câmera para a esquerda
            elif event.key == pygame.K_RIGHT:
                camera_offset_x += 10  # Mover a câmera para a direita
            elif event.key == pygame.K_w:
                camera_offset_y -= 10  # Mover a câmera para cima
            elif event.key == pygame.K_s:
                camera_offset_y += 10  # Mover a câmera para baixo
        elif event.type == pygame.MOUSEWHEEL:
            angular_velocity += event.y * 0.002
            angular_velocity = max(0.001, angular_velocity)

# Função para desenhar o HUD


def display_hud():
    font = pygame.font.Font(None, 30)
    text = font.render(f"a: {a}, b: {b}, Vel. Angular: {
                       angular_velocity:.3f}", True, WHITE)
    screen.blit(text, (10, 10))

# Função principal de renderização


def render():
    global angle

    # Atualizar o ângulo
    angle += angular_velocity
    if angle >= 2 * math.pi:
        angle -= 2 * math.pi

    # Calcular a posição do satélite para órbita elíptica
    satellite_x = center_x + a * math.cos(angle)
    satellite_y = center_y + b * math.sin(angle)

    # Adicionar o ponto à lista de trajetória
    orbit_points.append((satellite_x, satellite_y))
    if len(orbit_points) > 1000:
        orbit_points.pop(0)

    # Desenhar na tela
    screen.fill(BLACK)

    # Desenhar a órbita do satélite (sem a linha elíptica)
    if show_orbit_path and len(orbit_points) > 1:
        # Ajustando o caminho do satélite para simular a movimentação da câmera
        adjusted_orbit_points = [
            (x - camera_offset_x, y - camera_offset_y) for x, y in orbit_points]
        pygame.draw.lines(screen, WHITE, False, adjusted_orbit_points, 1)

    # Desenhar o planeta com imagem (a Terra é fixa no centro)
    earth_rect = earth_image.get_rect(
        center=(center_x - camera_offset_x, center_y - camera_offset_y))
    screen.blit(earth_image, earth_rect.topleft)

    # Desenhar o satélite com imagem (ajustando para o deslocamento da câmera)
    satellite_rect = satellite_image.get_rect(
        center=(satellite_x - camera_offset_x, satellite_y - camera_offset_y))
    screen.blit(satellite_image, satellite_rect.topleft)

    # Exibir HUD
    display_hud()

    # Atualizar a tela
    pygame.display.flip()


# Loop principal
while running:
    handle_events()
    render()
    clock.tick(60)

# Encerrar Pygame
pygame.quit()
sys.exit()
