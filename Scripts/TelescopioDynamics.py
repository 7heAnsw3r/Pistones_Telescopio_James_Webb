import tkinter as tk
from tkinter import messagebox
from scipy.optimize import minimize
import numpy as np
import matplotlib.pyplot as plt

# David tienes que corregir los bugs, ademas tienes que mejorar la interfaz donde el usuario ingresa los valores, por favor
# Tienes que quitar el B minimo a la interfaz ya que ese tiene que ser la mitad del maximo
# Ten en cuenta que te toca lo mas facil, asi que no nos decepciones por favor, hay mucho puede ser algo asi
# puede ser algo asi https://codigospython.com/python-para-la-programacion-de-interfaces-de-usuario-ui/ es solo una guia
# Si quieres hacerlo mejor pues bienvenido, Muestra los valores de la longitud de los pistones y el angulo del espejo


# Función de costo para la optimización
def costo(pos, A, B_min, B_max, C, x1, y1, F):
    x2, y2 = pos
    PA1_base = np.array([-A / 2, 0])
    PA2_base = np.array([A / 2, 0])
    espejo_primario = np.array([PA1_base[0] + F, 0])  # Espejo primario fijo

    vector_P = np.array([x1 - x2, y1 - y2])
    vector_L = np.array([-(y1 - y2), x1 - x2])

    norm_vector_L = np.linalg.norm(vector_L)
    if norm_vector_L < 1e-6:
        vector_L_normalizado = np.array([0, 0])
    else:
        vector_L_normalizado = vector_L / norm_vector_L

    PA3_espejo = np.array([x2 - (C / 2) * vector_L_normalizado[0], y2 - (C / 2) * vector_L_normalizado[1]])
    PA4_espejo = np.array([x2 + (C / 2) * vector_L_normalizado[0], y2 + (C / 2) * vector_L_normalizado[1]])

    piston1 = np.linalg.norm(PA3_espejo - PA1_base)
    piston2 = np.linalg.norm(PA4_espejo - PA2_base)
    angulo_P = np.degrees(np.arctan2(vector_P[1], vector_P[0]))

    # Penalización por longitud de los pistones
    penalizacion_longitud = 0
    if not (B_min <= piston1 <= B_max):
        penalizacion_longitud += abs(piston1 - B_max) if piston1 > B_max else abs(piston1 - B_min)
    if not (B_min <= piston2 <= B_max):
        penalizacion_longitud += abs(piston2 - B_max) if piston2 > B_max else abs(piston2 - B_min)

    # Penalización por ángulo fuera del rango permitido
    penalizacion_angulo = 0
    if not (0 <= angulo_P <= 180):
        penalizacion_angulo += abs(angulo_P - 90)

    # Penalización por no alinearse con el espejo primario
    vector_P_3D = np.array([vector_P[0], vector_P[1], 0])
    vector_espejo_3D = np.array([espejo_primario[0] - x2, espejo_primario[1] - y2, 0])
    alineacion = np.linalg.norm(np.cross(vector_P_3D, vector_espejo_3D)) / np.linalg.norm(vector_P_3D)

    return alineacion + penalizacion_longitud + penalizacion_angulo


# Función para graficar y optimizar el telescopio
def prototipo_telescopio(A, B_min, B_max, C, F, x1, y1):
    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 10))

    def update_plot(event):
        # Limitar la posición del mouse
        x1_new, y1_new = event.xdata, event.ydata

        if x1_new is None or y1_new is None:
            return

        # Optimización con la nueva posición del mouse
        x2_inicial, y2_inicial = 0, 3.0
        resultado = minimize(
            costo,
            [x2_inicial, y2_inicial],
            args=(A, B_min, B_max, C, x1_new, y1_new, F),
            bounds=[(-10, 10), (0, 15)]
        )

        x2_opt, y2_opt = resultado.x

        PA1_base = np.array([-A / 2, 0])
        PA2_base = np.array([A / 2, 0])
        espejo_primario = np.array([PA1_base[0] + F, 0])
        vector_P = np.array([x1_new - x2_opt, y1_new - y2_opt])
        vector_L = np.array([-(y1_new - y2_opt), x1_new - x2_opt])

        norm_vector_L = np.linalg.norm(vector_L)
        if norm_vector_L < 1e-6:
            vector_L_normalizado = np.array([0, 0])
        else:
            vector_L_normalizado = vector_L / norm_vector_L

        PA4_espejo = np.array([x2_opt - (C / 2) * vector_L_normalizado[0], y2_opt - (C / 2) * vector_L_normalizado[1]])
        PA3_espejo = np.array([x2_opt + (C / 2) * vector_L_normalizado[0], y2_opt + (C / 2) * vector_L_normalizado[1]])

        piston1 = np.linalg.norm(PA3_espejo - PA1_base)
        piston2 = np.linalg.norm(PA4_espejo - PA2_base)
        angulo_P = np.degrees(np.arctan2(vector_P[1], vector_P[0]))

        # Limpiar y graficar resultados
        ax.clear()
        ax.plot(PA1_base[0], PA1_base[1], 'go', label="PA1")
        ax.plot(PA2_base[0], PA2_base[1], 'bo', label="PA2")
        ax.plot(PA3_espejo[0], PA3_espejo[1], 'mo', label="PA3")
        ax.plot(PA4_espejo[0], PA4_espejo[1], 'co', label="PA4")
        ax.plot(espejo_primario[0], espejo_primario[1], 'ks', label="Espejo Primario")
        ax.plot(x2_opt, y2_opt, 'ro', label="Punto medio del espejo")
        ax.plot([PA1_base[0], PA3_espejo[0]], [PA1_base[1], PA3_espejo[1]], 'g--', label=f"Pistón 1")
        ax.plot([PA2_base[0], PA4_espejo[0]], [PA2_base[1], PA4_espejo[1]], 'b--', label=f"Pistón 2")
        ax.plot([-A / 2, A / 2], [0, 0], 'k-', label="Base del telescopio")
        ax.plot([PA3_espejo[0], PA4_espejo[0]], [PA3_espejo[1], PA4_espejo[1]], 'r-', label="Espejo Secundario")
        ax.plot(x1_new, y1_new, 'r*', markersize=12, label="Punto P")
        ax.quiver(x2_opt, y2_opt, vector_P[0], vector_P[1], angles='xy', scale_units='xy', scale=1, color='orange',
                  label=r"$\vec{P}$")
        ax.quiver(x2_opt, y2_opt, vector_L[0], vector_L[1], angles='xy', scale_units='xy', scale=1, color='purple',
                  label=r"$\vec{L}$")
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Telescopio Espacial')
        ax.grid()
        ax.legend()
        ax.axis('equal')
        ax.set_xlim(-10, 10)
        ax.set_ylim(-2, 15)
        plt.draw()

    # Conectar la función de actualización del mouse
    fig.canvas.mpl_connect('motion_notify_event', update_plot)

    # Mostrar la figura inicialmente
    plt.show()


# Función para crear la interfaz gráfica
def crear_interfaz():
    def on_submit():
        try:
            A = float(entry_A.get())
            B_min = float(entry_B_min.get())
            B_max = float(entry_B_max.get())
            C = float(entry_C.get())  # Nuevo campo para C
            F = 3
            x1 = -2
            y1 = 6.5
            prototipo_telescopio(A, B_min, B_max, C, F, x1, y1)
            root.destroy()
        except ValueError:
            messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos.")

    root = tk.Tk()
    root.title("Configuración del Telescopio")

    # Labels and entry fields
    tk.Label(root, text="Valor de A:").pack(padx=10, pady=5)
    entry_A = tk.Entry(root)
    entry_A.pack(padx=10, pady=5)

    tk.Label(root, text="Valor de B_min:").pack(padx=10, pady=5)
    entry_B_min = tk.Entry(root)
    entry_B_min.pack(padx=10, pady=5)

    tk.Label(root, text="Valor de B_max:").pack(padx=10, pady=5)
    entry_B_max = tk.Entry(root)
    entry_B_max.pack(padx=10, pady=5)

    tk.Label(root, text="Valor de C:").pack(padx=10, pady=5)
    entry_C = tk.Entry(root)
    entry_C.pack(padx=10, pady=5)

    # Submit button
    submit_button = tk.Button(root, text="Iniciar", command=on_submit)
    submit_button.pack(pady=10)

    root.mainloop()


# Iniciar la interfaz gráfica
crear_interfaz()

