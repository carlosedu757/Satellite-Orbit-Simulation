import pygame
import math
import sys

# Configurações da tela
WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SATELLITE_COLOR = (255, 0, 0)
PLANET_COLOR = (0, 0, 255)

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação de Órbita do Satélite")
clock = pygame.time.Clock()

# Parâmetros da órbita
center_x, center_y = WIDTH // 2, HEIGHT // 2  # Centro do planeta
radius = 200  # Raio da órbita
angle = 0  # Ângulo inicial
angular_velocity = 0.01  # Velocidade angular

# Loop principal
running = True
show_orbit_path = True
orbit_points = []  # Armazena os pontos da órbita para desenhar a linha

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Tecla para alternar a exibição da órbita
                show_orbit_path = not show_orbit_path
            elif event.key == pygame.K_UP:  # Aumentar o raio da órbita
                radius += 10
            elif event.key == pygame.K_DOWN:  # Diminuir o raio da órbita
                radius = max(50, radius - 10)  # Impedir que o raio seja muito pequeno

        elif event.type == pygame.MOUSEWHEEL:  # Alterar a velocidade angular
            angular_velocity += event.y * 0.002  # Aumentar/diminuir dependendo da direção
            angular_velocity = max(0.001, angular_velocity)  # Impedir valores negativos ou nulos

    # Atualizar o ângulo
    angle += angular_velocity
    if angle >= 2 * math.pi:
        angle -= 2 * math.pi

    # Calcular a posição do satélite
    satellite_x = center_x + radius * math.cos(angle)
    satellite_y = center_y + radius * math.sin(angle)

    # Adicionar o ponto à lista de trajetória
    orbit_points.append((satellite_x, satellite_y))
    if len(orbit_points) > 1000:  # Limitar o número de pontos armazenados
        orbit_points.pop(0)

    # Desenhar na tela
    screen.fill(BLACK)  # Limpa a tela

    # Desenhar o planeta
    pygame.draw.circle(screen, PLANET_COLOR, (center_x, center_y), 20)

    # Desenhar a trajetória da órbita
    if show_orbit_path:
        if len(orbit_points) > 1:
            pygame.draw.lines(screen, WHITE, False, orbit_points, 1)

    # Desenhar o satélite
    pygame.draw.circle(screen, SATELLITE_COLOR, (int(satellite_x), int(satellite_y)), 5)

    # Atualizar a tela
    pygame.display.flip()
    clock.tick(60)

# Encerrar Pygame
pygame.quit()
sys.exit()
