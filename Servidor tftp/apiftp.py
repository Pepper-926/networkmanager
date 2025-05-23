from ftplib import FTP

def listar_contenido(ftp):
    """Lista el contenido del directorio actual en el servidor FTP."""
    try:
        contenido = ftp.nlst()
        carpetas = []
        archivos = []

        for elemento in contenido:
            try:
                # Intentar cambiar al directorio para verificar si es carpeta
                ftp.cwd(elemento)
                carpetas.append(elemento)
                ftp.cwd('..')  # Volver al directorio anterior
            except Exception:
                # Si no puede cambiar al directorio, es un archivo
                archivos.append(elemento)

        print("\nContenido del directorio actual:")
        print("Carpetas:")
        for carpeta in carpetas:
            print(f"  [D] {carpeta}")
        print("Archivos:")
        for archivo in archivos:
            print(f"  [F] {archivo}")
        return carpetas, archivos
    except Exception as e:
        print(f"Error al listar contenido: {e}")
        return [], []


def leer_archivo_txt(ftp, archivo):
    """Lee y muestra el contenido de un archivo .txt desde el servidor FTP."""
    try:
        print(f"\nLeyendo archivo: {archivo}")
        with open('temp.txt', 'wb') as f:
            ftp.retrbinary(f"RETR {archivo}", f.write)

        # Leer el contenido del archivo temporal
        with open('temp.txt', 'r') as f:
            contenido = f.read()
            print(f"\nContenido de {archivo}:\n{'-' * 50}\n{contenido}\n{'-' * 50}")
    except Exception as e:
        print(f"Error al leer archivo {archivo}: {e}")


def explorar_ftp(servidor, usuario, contraseña):
    try:
        # Conectar al servidor FTP
        ftp = FTP(servidor)
        ftp.login(user=usuario, passwd=contraseña)
        print(f"Conectado a {servidor} como {usuario}")

        while True:
            # Listar contenido del directorio actual
            carpetas, archivos = listar_contenido(ftp)

            # Mostrar opciones al usuario
            print("\nOpciones:")
            print("  [0] Salir")
            if ftp.pwd() != '/':
                print("  [..] Subir al directorio anterior")
            for i, carpeta in enumerate(carpetas, start=1):
                print(f"  [{i}] Abrir carpeta '{carpeta}'")
            for j, archivo in enumerate(archivos, start=len(carpetas) + 1):
                print(f"  [{j}] Leer archivo '{archivo}'")

            # Leer opción del usuario
            opcion = input("Selecciona una opción: ")

            if opcion == "0":
                print("Saliendo del explorador FTP.")
                break
            elif opcion == ".." and ftp.pwd() != '/':
                ftp.cwd('..')  # Subir al directorio anterior
            elif opcion.isdigit():
                opcion = int(opcion)
                if 1 <= opcion <= len(carpetas):
                    # Cambiar al directorio seleccionado
                    ftp.cwd(carpetas[opcion - 1])
                elif len(carpetas) < opcion <= len(carpetas) + len(archivos):
                    # Leer el archivo seleccionado
                    archivo_seleccionado = archivos[opcion - len(carpetas) - 1]
                    if archivo_seleccionado.endswith('.txt'):
                        leer_archivo_txt(ftp, archivo_seleccionado)
                    else:
                        print(f"El archivo '{archivo_seleccionado}' no es un archivo .txt.")
                else:
                    print("Opción no válida. Intenta de nuevo.")
            else:
                print("Opción no válida. Intenta de nuevo.")

        # Cerrar conexión
        ftp.quit()
        print("Conexión cerrada.")

    except Exception as e:
        print(f"Error: {e}")


# Configuración del servidor FTP
servidor = "127.0.0.1"
usuario = "Gabriel"
contraseña = "Pepper_926"

# Explorar el servidor FTP
explorar_ftp(servidor, usuario, contraseña)