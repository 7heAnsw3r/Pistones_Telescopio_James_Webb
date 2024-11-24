import sys
import random
import numpy as np
import pygame
from scipy.optimize import minimize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout,
    QHBoxLayout, QWidget
)
from PyQt6.QtGui import QPixmap


class TelescopioApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulación Telescopio James Webb")
        self.setGeometry(100, 100, 800, 400)
        self.A = self.B = self.C = None  # Variables del telescopio
        self.init_ui()

    def init_ui(self):
        # Layout principal dividido en columnas
        main_layout = QHBoxLayout()

        # Columna izquierda: Campos de entrada
        input_layout = QVBoxLayout()
        input_layout.addWidget(QLabel("Ingresa el valor de A (positivo):"))
        self.input_a = QLineEdit()
        input_layout.addWidget(self.input_a)

        input_layout.addWidget(QLabel("Ingresa el valor de B (positivo):"))
        self.input_b = QLineEdit()
        input_layout.addWidget(self.input_b)

        input_layout.addWidget(QLabel("Ingresa el valor de C (positivo):"))
        self.input_c = QLineEdit()
        input_layout.addWidget(self.input_c)

        self.start_button = QPushButton("Iniciar Simulación")
        self.start_button.clicked.connect(self.start_simulation)
        input_layout.addWidget(self.start_button)

        # Columna derecha: Imagen o texto
        right_layout = QVBoxLayout()
        self.image_label = QLabel()
        pixmap = QPixmap("../Imagenes/telescopio.png")  # Imagen del telescopio
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(300, 300))
        else:
            self.image_label.setText("Imagen no encontrada")
        right_layout.addWidget(self.image_label)

        self.quote_label = QLabel("Explorando los misterios del universo 🚀")
        self.quote_label.setStyleSheet("font-size: 16px; color: #555;")
        right_layout.addWidget(self.quote_label)

        # Combinar los layouts
        main_layout.addLayout(input_layout)
        main_layout.addLayout(right_layout)

        # Configurar la ventana principal
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def start_simulation(self):
        try:
            # Validar entrada de datos
            self.A = float(self.input_a.text())
            self.B = float(self.input_b.text())
            self.C = float(self.input_c.text())

            if self.A <= 0 or self.B <= 0 or self.C <= 0:
                raise ValueError("Todos los valores deben ser positivos.")

            # Iniciar la simulación en Pygame
            iniciar_simulacion_pygame(self.A, self.B, self.C)

        except ValueError as e:
            self.statusBar().showMessage(f"Error: {e}")


def costo(pos, A, B, C, x1, y1):
    x2, y2 = pos
    PA1_base = np.array([-A / 2, 0])
    PA2_base = np.array([A / 2, 0])
    
    vector_P = np.array([x1 - x2, y1 - y2])
    vector_L = np.array([-(y1 - y2), x1 - x2])
    
    # Asegurarse de que la normalización no cause un problema por división por cero
    norm_vector_L = np.linalg.norm(vector_L)
    if norm_vector_L < 1e-6:  # Si la magnitud del vector es muy pequeña
        vector_L_normalizado = np.array([0, 0])  # Evitar la división por cero
    else:
        vector_L_normalizado = vector_L / norm_vector_L  # Normalizar correctamente
    
    PA3_espejo = np.array([x2 - (C / 2) * vector_L_normalizado[0], y2 - (C / 2) * vector_L_normalizado[1]])
    PA4_espejo = np.array([x2 + (C / 2) * vector_L_normalizado[0], y2 + (C / 2) * vector_L_normalizado[1]])
    
    piston1 = np.linalg.norm(PA3_espejo - PA1_base)
    piston2 = np.linalg.norm(PA4_espejo - PA2_base)
    angulo_P = np.degrees(np.arctan2(vector_P[1], vector_P[0]))
    
    perpendicularidad = abs(np.dot(vector_P, vector_L))
    penalizacion_longitud = 0
    if not (B / 2 <= piston1 <= B):
        penalizacion_longitud += abs(piston1 - B) if piston1 > B else abs(piston1 - B / 2)
    if not (B / 2 <= piston2 <= B):
        penalizacion_longitud += abs(piston2 - B) if piston2 > B else abs(piston2 - B / 2)
    
    penalizacion_angulo = 0
    if not (0 <= angulo_P <= 180):
        penalizacion_angulo += abs(angulo_P - 90)
    
    return perpendicularidad + penalizacion_longitud + penalizacion_angulo

def iniciar_simulacion_pygame(A, B, C):
    """
    Simulación dinámica en Pygame para mostrar el funcionamiento del telescopio.
    """
    pygame.init()
    size = (800, 600)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Simulación del Telescopio")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    # Coordenadas de estrellas
    star_coordinates = [[random.randint(0, 800), random.randint(0, 600)] for _ in range(100)]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Posición del ratón y optimización
        mouse_pos = pygame.mouse.get_pos()
        resultado = minimize(costo, [0, 7.5], args=(A, B, C, mouse_pos[0] / 100 - 4, 15 - mouse_pos[1] / 40))
        x2_opt, y2_opt = resultado.x

        # Dibujar fondo, estrellas y telescopio
        screen.fill((0, 0, 0))
        for coordinates in star_coordinates:
            pygame.draw.circle(screen, (255, 255, 255), coordinates, 2)
            coordinates[1] += 1
            if coordinates[1] > 600:
                coordinates[1] = 0

        base_x, base_y = 400, 600
        if x2_opt is not None:
            pygame.draw.rect(screen, (128, 128, 128), (base_x - A * 25, base_y - 10, A * 50, 20))
            pygame.draw.rect(screen, (255, 0, 0), (base_x - A * 25, base_y - 10, 5, -(y2_opt * 40)))
            pygame.draw.rect(screen, (255, 0, 0), (base_x + A * 25 - 5, base_y - 10, 5, -(y2_opt * 40)))
            espejo_x = base_x + x2_opt * 100
            espejo_y = base_y - y2_opt * 40
            pygame.draw.circle(screen, (0, 0, 255), (int(espejo_x), int(espejo_y)), int(C * 20))
            pygame.draw.line(screen, (255, 255, 0), (base_x - A * 25, base_y), (espejo_x, espejo_y), 2)
            pygame.draw.line(screen, (255, 255, 0), (base_x + A * 25, base_y), (espejo_x, espejo_y), 2)

        # Mostrar texto informativo
        info_text = f"A: {A:.2f}, B: {B:.2f}, C: {C:.2f}, x: {x2_opt:.2f}, y: {y2_opt:.2f}"
        text_surface = font.render(info_text, True, (255, 255, 255))
        screen.blit(text_surface, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TelescopioApp()
    ventana.show()
    sys.exit(app.exec())