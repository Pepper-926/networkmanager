import os

def crear_carpeta(directorio, nombre_carpeta):
    """
    Crea una carpeta en el directorio especificado.

    Args:
        directorio (str): Ruta del directorio donde se creará la carpeta.
        nombre_carpeta (str): Nombre de la carpeta a crear.
    """
    # Construir la ruta completa de la nueva carpeta
    ruta_carpeta = os.path.join(directorio, nombre_carpeta)
    
    try:
        # Crear la carpeta si no existe
        os.makedirs(ruta_carpeta, exist_ok=True)
        print(f"Carpeta '{nombre_carpeta}' creada en: {ruta_carpeta}")
    except Exception as e:
        print(f"Error al crear la carpeta: {e}")

# Ejemplo de uso
if __name__ == "__main__":
    # Solicitar al usuario el directorio y el nombre de la carpeta
    ruta_directorio = input("Introduce el directorio donde deseas crear la carpeta: ")
    nombre_carpeta = input("Introduce el nombre de la carpeta: ")

    # Crear la carpeta
    crear_carpeta(ruta_directorio, nombre_carpeta)
