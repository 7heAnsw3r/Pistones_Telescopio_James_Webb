import subprocess
import sys

def install_requirements():
    """
    Lee el archivo 'requirements.txt', extrae las librerías mencionadas en cada línea e instala 
    cada una de ellas utilizando pip.
    
    El archivo 'requirements.txt' debe contener una lista de librerías, una por línea.

    No retorna nada. Si alguna de las instalaciones falla, la función lanzará una excepción.

    Excepciones:
        subprocess.CalledProcessError: Si alguna instalación falla, esta excepción será lanzada.
    """
    # Abre el archivo requirements.txt y lee las líneas
    with open('requirements.txt', 'r') as file:
        libraries = file.readlines()
    
    # Instala cada librería usando pip
    for library in libraries:
        library = library.strip()  # Eliminar espacios en blanco y saltos de línea
        if library:  # Asegurarse de que no esté vacío
            print(f"Instalando {library}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", library])

if __name__ == "__main__":
    install_requirements()
