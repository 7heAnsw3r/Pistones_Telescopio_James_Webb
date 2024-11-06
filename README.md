# 🔭 Proyecto de Métodos Numéricos: Orientación del Espejo Secundario del Telescopio

Este proyecto aborda el diseño de un modelo simplificado del mecanismo de ajuste del espejo secundario en el telescopio James Webb. Usaremos un enfoque de métodos numéricos para calcular la extensión de dos pistones lineales que permiten orientar el espejo secundario hacia un punto específico en el espacio.

## 📄 Descripción del Proyecto

El objetivo principal es determinar las extensiones de dos pistones que ajustan un espejo secundario de forma rectangular para que se oriente de forma perpendicular hacia un punto en el espacio, definido por sus coordenadas \( P(x, y) \). El cálculo debe respetar los límites de extensión de los pistones y la distancia entre ellos.

## 🎯 Objetivo del Proyecto

- **🔧 Cálculo de Extensiones de Pistones:** Usar métodos numéricos para calcular las distancias de los pistones necesarias para orientar el espejo.
- **💻 Interfaz Gráfica:** Desarrollar una interfaz que permita ingresar parámetros y visualizar la orientación del espejo.

## 📊 Parámetros de Entrada y Salida

### 🔹 Entrada
- **L**: Largo del espejo secundario (en metros).
- **B**: Distancia entre los puntos de anclaje de los pistones en la base (en metros).
- **d_min** y **d_max**: Longitudes mínima y máxima permitidas de cada pistón.
- **P(x, y)**: Coordenadas del punto objetivo en el espacio (en metros).

### 🔸 Salida
- **x1**: Longitud del Pistón 1 (en metros).
- **x2**: Longitud del Pistón 2 (en metros).

## 🛠️ Tecnologías y Herramientas

- **📝 Lenguaje de Programación**: Python.
- **📐 Librerías**: `numpy`, `scipy`, `matplotlib` para cálculos y visualización; `tkinter` para la interfaz gráfica.
- **📅 Colaboración**: Usaremos GitHub Projects para gestionar tareas y el avance del proyecto.
