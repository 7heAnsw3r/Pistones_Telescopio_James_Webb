import subprocess
import sys

def install_requirements():
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
