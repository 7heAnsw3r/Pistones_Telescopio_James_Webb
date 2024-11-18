import pygame
import sys
import random
import math
from scipy.optimize import minimize
import numpy as np

# Inicializar Pygame
pygame.init()

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Especificaciones de pantalla
size = (800, 600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Interfaz Gráfica: Telescopio")
clock = pygame.time.Clock()

# Estrellas
num_stars = 100
size_star = 4
star_coordinates = []

# Generar coordenadas iniciales para las estrellas
for _ in range(num_stars):
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    star_coordinates.append([x, y])

# Función para dibujar una estrella
def draw_star(screen, color, center, size):
    points = []
    num_points = 5  # Número de puntas de la estrella
    angle = 2 * math.pi / (num_points * 2)  # Ángulo para alternar puntas grandes y pequeñas
    for i in range(num_points * 2):
        r = size if i % 2 == 0 else size // 2  # Alternar entre punta larga y corta
        x = center[0] + int(r * math.cos(i * angle))
        y = center[1] + int(r * math.sin(i * angle))
        points.append((x, y))
    pygame.draw.polygon(screen, color, points)

# Funciones del telescopio
def costo(pos, A, B, C, x1, y1):
    x2, y2 = pos
    PA1_base = np.array([-A / 2, 0])
    PA2_base = np.array([A / 2, 0])
    vector_P = np.array([x1 - x2, y1 - y2])
    vector_L = np.array([-(y1 - y2), x1 - x2])
    norm_vector_L = np.linalg.norm(vector_L)
    vector_L_normalizado = vector_L / norm_vector_L if norm_vector_L > 1e-6 else np.array([0, 0])
    PA3_espejo = np.array([x2 - (C / 2) * vector_L_normalizado[0], y2 - (C / 2) * vector_L_normalizado[1]])
    PA4_espejo = np.array([x2 + (C / 2) * vector_L_normalizado[0], y2 + (C / 2) * vector_L_normalizado[1]])
    piston1 = np.linalg.norm(PA3_espejo - PA1_base)
    piston2 = np.linalg.norm(PA4_espejo - PA2_base)
    perpendicularidad = abs(np.dot(vector_P, vector_L))
    penalizacion_longitud = (
        max(0, abs(piston1 - B) if piston1 > B else B / 2 - piston1) +
        max(0, abs(piston2 - B) if piston2 > B else B / 2 - piston2)
    )
    return perpendicularidad + penalizacion_longitud

def restriccion_angulo(pos, x1, y1):
    x2, y2 = pos
    vector_P = np.array([x1 - x2, y1 - y2])
    angulo_P = np.degrees(np.arctan2(vector_P[1], vector_P[0]))
    return 180 - abs(angulo_P)

def optimizar_telescopio(A, B, C, x1, y1):
    x2_inicial, y2_inicial = 0, 3.0
    restricciones = ({
        'type': 'ineq',
        'fun': restriccion_angulo,
        'args': (x1, y1)
    })
    resultado = minimize(
        costo,
        [x2_inicial, y2_inicial],
        args=(A, B, C, x1, y1),
        bounds=[(-10, 10), (0, 15)],
        constraints=restricciones
    )
    return resultado.x if resultado.success else (None, None)

# Variables del telescopio
A, B, C = 4, 5, 2
x1, y1 = 0, 6  # Coordenadas de la estrella

# Bucle principal
running = True
pygame.mouse.set_visible(False)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Obtener posición del mouse
    mouse_pos = pygame.mouse.get_pos()
    x1, y1 = mouse_pos[0] / 100 - 4, 15 - mouse_pos[1] / 40  # Convertir a coordenadas del telescopio
    print(x1, y1)
    # Optimizar posición del telescopio
    x2_opt, y2_opt = optimizar_telescopio(A, B, C, x1, y1)

    # Llenar pantalla con color negro
    screen.fill(black)

    # Dibujar estrellas y moverlas hacia abajo
    for coordinates in star_coordinates:
        draw_star(screen, white, coordinates, size_star)
        coordinates[1] += 0.3
        if coordinates[1] > size[1]:
            coordinates[1] = 0

    # Dibujar telescopio si es válido
    if x2_opt is not None:
        pygame.draw.line(screen, blue, (400 - A * 25, 600), (400 + A * 25, 600), 3)  # Base
        pygame.draw.line(screen, red, (400 - A * 25, 600), (x2_opt * 100 + 400, 600 - y2_opt * 40), 2)  # Pistón 1
        pygame.draw.line(screen, red, (400 + A * 25, 600), (x2_opt * 100 + 400, 600 - y2_opt * 40), 2)  # Pistón 2

    # Dibujar estrella objetivo
    draw_star(screen, red, mouse_pos, size_star * 2)

    # Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
