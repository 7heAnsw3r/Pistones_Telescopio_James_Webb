# 🔭 Proyecto de Métodos Numéricos: Orientación del Espejo Secundario del Telescopio

Este proyecto aborda el diseño de un modelo simplificado del mecanismo de ajuste del espejo secundario en el telescopio James Webb. Usaremos un enfoque de métodos numéricos para calcular la extensión de dos pistones lineales que permiten orientar el espejo secundario hacia un punto específico en el espacio.

---

## Tabla de Contenidos
1. [Introducción](#descripción-del-Proyecto)
2. [Requisitos Previos](#objetivo-del-proyecto)
3. [Instalación](#instalación)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Uso](#uso)
6. [Documentación del Código](#documentación-del-código)

---

## 📄 Descripción del Proyecto

El proyecto busca orientar el espejo secundario de un telescopio perpendicularmente a un punto cuyo movimiento es controlado mediante la posición del mouse, esto mediante el movimiento de dos pistones con extensión predefinida anclados a una base de longitud variable.

## 🎯 Objetivo del Proyecto

- **🔧 Cálculos Matemáticos:** Usar métodos numéricos para determinar la posicion del espejo y los pistones para ajustarse de manera perpendicular a la estrella.
- **💻 Interfaz Gráfica:** Desarrollar una interfaz que permita ingresar parámetros y visualizar la orientación del espejo de manera dinámica.

---

## 🛠️ Instalacción

**Requisitos previos:**
* Sistema operativo Linux o Windows.
* Tener Python3 Instalado.
* Tener instalado Pip3.

Para hacer uso del código debemos seguir los siguientes pasos, ya sea en la consola propia del sistema operativo Linux, PowerShell o La consola de Visual Studio Code:
- **Clonar el repositorio:**
```shell
git clone https://github.com/7heAnsw3r/Pistones_Telescopio_James_Webb.git
```
- **Instalar librerias requeridas**
Debe Colocarse en el direcctorio clonado previamente
```shell
cd Pistones_Telescopio_James_Webb/Requerimientos
```
y posteriormente ejecutar el script llamado `Instalar_requerimientos.py` de la siguiente manera (Linux: usar `sudo` en caso de requerir permisos de super usuario):
```shell
python3 install_requirements.py
```

---

## 📂 Estructura del proyecto

**Directorios y Ficheros:**  
El repositorio está seccionado por carpetas, las cuales tienen nombres descriptivos que señalan lo que contienen:
- En la raíz tenemos un notebook con el desarrollo del sistema de ecuaciones y un archivo README.md.
- El directorio **Imagenes** contiene ilustraciones representativas del telescopio del cual basamos el prototipo.
- El directorio **Requerimientos** contiene los archivos necesarios para instalar las librerías requeridas por el programa.
- El directorio **Scripts** contiene los códigos de las aplicaciones desarrolladas para el proyecto, una simulación en fase Beta y el código principal `TelescopioDynamics.py`.

**Estructura del código**
Este basa su estructura en funciones cada una una descrita mediante el uso de **DocStrings**.

---

## ▶️ Uso
**Windows:**
Para ejecutar el programa en Windows podemos hacer uso de una aplicación que compile código, como por ejemplo: Visual Studio Code o ejecutando el siguiente comando desde la PowerShell de Windows desde el direcctorio que contiene al programa:
```shell
python TelescopioDynamics.py
```

**Linux**
Simplemente ejecutamos el siguiente comando desde la Terminal:
```shell
python3 TelescopioDynamics.py
```
**Indicaciones:**
Una vez ejecutado seguir los siguientes pasos:
- Esperar que aparezca la interfaz gráfica.
- Ingresar los datos requeridos en la interfaz, respetando las restricciones.
- Iniciar la simulación.
- Interactuar con el programa.

---

## 🧩 Documentación del Código

Como se dijo antes las funciones ya contienen DocStrings, herramienta de documentación para el código el cual nos dice de manera clara el uso de la función, sus parametros de entrada y lo que retorna; o que acción realiza en caso de no retornar valores.  
Sin Embargo, vamos a explorar más a detalle las características de las funciones mas importantes del código:  
### **Función Costo**
```python
def costo(pos, A, B_min, B_max, C, x1, y1, F):
    """
    Calcula el costo de un sistema de pistones para el control de la longitud de los pistones, 
    el ángulo de un espejo y la alineación con el Foco. La función penaliza configuraciones que 
    no cumplan con ciertos rangos establecidos.

    Args:
        pos (tuple): Tupla de dos elementos (x2, y2) que representa la posición inicial de la estructura.
        A (float): Ancho total de la estructura Base.
        B_min (float): Longitud mínima permitida para los pistones.
        B_max (float): Longitud máxima permitida para los pistones.
        C (float): Factor para determinar la longitud de ajuste del espejo.
        x1 (float): Coordenada x de la estrella.
        y1 (float): Coordenada y de la estrella.
        F (float): Foco del Espejo Primario.

    Returns:
        float: Aliniacion con el foco del espejo primario, penalizacion de longitud para los pistones y para el angulo del espejo.
    """
    x2, y2 = pos
    PA1_base = np.array([-A / 2, 0])  # Aseguramos que PA1 esté a la izquierda del origen
    PA2_base = np.array([A / 2, 0])   # PA2 estará a la derecha del origen
    espejo_primario = np.array([0 + F, 0])  # Espejo primario ajustado respecto al origen

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
```

#### Cálculos Realizados
1. **Alineación con el Foco**:
   Se calcula la **distancia perpendicular** entre el vector de orientación del espejo y el vector hacia el foco (usando el producto cruzado entre vectores en 3D).
   
2. **Penalización por Longitud de los Pistones**:
   Se calcula la distancia de los pistones y se compara con los rangos permitidos (`B_min` y `B_max`). Si las longitudes no están dentro del rango, se aplica una penalización proporcional a la desviación.

3. **Penalización por Ángulo**:
   Se calcula el **ángulo** entre el vector hacia el punto objetivo y el eje de orientación. Si el ángulo se encuentra fuera del rango de 0 a 180 grados, se penaliza con la diferencia respecto a los 90 grados.

#### Resultado Final
La función retorna la **suma de las penalizaciones** por alineación, longitud de pistones y ángulo. Un valor más bajo indica una configuración más óptima, mientras que valores más altos sugieren que el sistema está fuera de los rangos deseados

### **Función Telescopio**
```python
def telescopio(A, B_min, B_max, C, F):
    """
    Genera y muestra una visualización interactiva de un telescopio espacial, donde la posición de una estrella 
    puede ser movida con el mouse. A medida que la estrella se mueve, el sistema de 
    pistones se ajusta automáticamente utilizando un algoritmo de optimización, y los resultados se muestran 
    gráficamente en tiempo real.

    Args:
        A (float): Ancho total de la estructura Base.
        B_min (float): Longitud mínima permitida para los pistones.
        B_max (float): Longitud máxima permitida para los pistones.
        C (float): Factor para determinar la longitud de ajuste del espejo.
        F (float): Foco del Espejo Primario.
    
    Returns:
        No retorna, muestra una figura interactiva del telescopio.
    """
    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 10))

    def update_plot(event):
        """
        Actualiza la visualización del telescopio cuando el usuario mueve el mouse en la ventana gráfica.

        Args:
            event (matplotlib.backend_bases.MouseEvent): El evento del mouse que contiene las nuevas coordenadas 
                                                    de la estrella cuando se mueve el cursor.
        
        Returns:
        No retorna nada. Actualiza la gráfica en tiempo real con los nuevos valores calculados para la posición 
        del espejo y los pistones.
        """
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
        espejo_primario = np.array([0 + F, 0])
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
        ax.plot(x1_new, y1_new, 'r*', markersize=12, label="Estrella")
        ax.quiver(x2_opt, y2_opt, vector_P[0], vector_P[1], angles='xy', scale_units='xy', scale=1, color='orange',
                  label=r"$\vec{P}$")
        ax.quiver(x2_opt, y2_opt, vector_L[0], vector_L[1], angles='xy', scale_units='xy', scale=1, color='purple',
                  label=r"$\vec{L}$")

        # Añadir cuadro con la información relevante
        info_text = f"Coordenadas_Estrella: ({x1_new:.2f}, {y1_new:.2f})\n"
        info_text += f"Pistón 1: {piston1:.2f} m\nPistón 2: {piston2:.2f} m\nÁngulo_espejo: {angulo_P:.2f}°"
        ax.text(0.7, 1, info_text, transform=ax.transAxes, fontsize=12, verticalalignment='top',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.1'))

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
```
#### Cálculos Realizados en la Función `telescopio`

1. **Optimización de la Posición del Telescopio**:
   - La posición de la estrella (`x1_new`, `y1_new`) se obtiene mediante el movimiento del mouse.
   - Se utiliza la función `minimize` para encontrar las coordenadas óptimas de la base del telescopio (`x2_opt`, `y2_opt`), de manera que se minimice el "costo" de la configuración.

2. **Cálculo de las Coordenadas del Espejo Secundario**:
   - Se calculan las posiciones de los puntos `PA3_espejo` y `PA4_espejo`, que corresponden a los extremos del espejo secundario, a partir de las coordenadas óptimas obtenidas mediante la optimización y el ángulo calculado entre la estrella y el telescopio. Estos puntos se ajustan en función del **factor de ajuste del espejo** `C`.

3. **Cálculo de las Longitudes de los Pistones**:
   - La longitud de cada pistón (`piston1` y `piston2`) se calcula como la distancia entre los puntos `PA1_base` y `PA3_espejo`, y entre `PA2_base` y `PA4_espejo`, respectivamente, usando la norma de los vectores correspondientes.

4. **Cálculo del Ángulo del Espejo**:
   - El ángulo del espejo se calcula mediante la función `np.arctan2`, que determina el ángulo entre el vector de la estrella y el telescopio (`vector_P`), en relación con el eje horizontal (eje `x`). El valor resultante se convierte de radianes a grados utilizando `np.degrees`.

5. **Actualización y Visualización Gráfica**:
   - La visualización gráfica se actualiza en tiempo real utilizando `matplotlib`, mostrando la configuración actual del telescopio con los puntos relevantes: la base, los pistones, el espejo secundario, y la estrella.
   - Se dibujan las flechas que representan los vectores de orientación (`vector_P` y `vector_L`).

