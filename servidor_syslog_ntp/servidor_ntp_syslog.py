import socket
import struct
import time
import threading
from api_db import ApiDB

def handle_syslog(sock, buffer_size):
    """
    Maneja el servidor Syslog en un hilo separado.
    """
    print("Servidor Syslog iniciado.")
    try:
        while True:
            data, addr = sock.recvfrom(buffer_size)
            message = data.decode('utf-8').strip()
            
            print(f"Syslog - Mensaje recibido de {addr}: {message}")
            apidb.insertar_log(addr,message)

            with open("syslog_logs.txt", "a") as archivo:
                log_formateado = f"{addr}: {message}\n"
                archivo.write(log_formateado)
    except Exception as e:
        print(f"Error en el servidor Syslog: {e}")
    finally:
        sock.close()


def handle_ntp(sock):
    """
    Maneja el servidor NTP en un hilo separado.
    """
    print("Servidor NTP iniciado.")
    try:
        while True:
            data, addr = sock.recvfrom(48)  # Mensajes NTP son de 48 bytes
            if data:
                # Construir la respuesta NTP
                ntp_data = create_ntp_response(data)
                sock.sendto(ntp_data, addr)
                print(f"NTP - Respuesta enviada a {addr}")
    except Exception as e:
        print(f"Error en el servidor NTP: {e}")
    finally:
        sock.close()


def create_ntp_response(data):
    """
    Construye una respuesta NTP válida.
    """
    NTP_DELTA = 2208988800  # Tiempo de referencia (1 de enero de 1900)
    current_time = time.time() + NTP_DELTA

    # Desempaquetar la solicitud para validar su estructura (opcional)
    try:
        # Asegurarse de que el paquete recibido tiene el tamaño correcto
        if len(data) < 48:
            raise ValueError("Paquete de solicitud NTP demasiado pequeño.")

        # Empaquetar la respuesta NTP
        response = bytearray(48)
        response[0] = 0b00100100  # Leap indicator = 0, Version = 4, Mode = 4 (server)
        response[1] = 1  # Stratum nivel 1 (reloj de referencia)
        response[2] = 0  # Poll interval (8 bits)
        response[3] = 0xEC  # Precision (8 bits)

        # Campos adicionales para root delay, dispersion y identifier
        struct.pack_into('!I', response, 12, 0x4C434F43)  # "LOCL" para indicar un reloj local

        # Marcas de tiempo (en formato 64 bits)
        transmit_time = int(current_time)
        struct.pack_into('!I', response, 40, transmit_time)  # Transmit timestamp

        return response
    except Exception as e:
        print(f"Error al construir la respuesta NTP: {e}")
        return b'\x00' * 48  # Respuesta vacía en caso de error



def start_server(host='0.0.0.0', syslog_port=8514, ntp_port=8123, buffer_size=1048576):
    """
    Inicia el servidor combinado de Syslog y NTP.
    """
    try:
        # Crear y enlazar sockets para Syslog y NTP
        syslog_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        syslog_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, buffer_size)
        syslog_sock.bind((host, syslog_port))
        
        ntp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ntp_sock.bind((host, ntp_port))

        # Iniciar hilos para cada servicio
        threading.Thread(target=handle_syslog, args=(syslog_sock, buffer_size), daemon=True).start()
        threading.Thread(target=handle_ntp, args=(ntp_sock,), daemon=True).start()

        print(f"Servidor combinado iniciado en {host}. Syslog en {syslog_port}, NTP en {ntp_port}.")
        print("Presiona Ctrl+C para detener el servidor.")

        while True:
            time.sleep(1)  # Mantener el hilo principal activo

    except PermissionError:
        print("Error: Necesitas permisos de administrador para usar los puertos 514 (Syslog) y 123 (NTP).")
    except Exception as e:
        print(f"Ocurrió un error al iniciar el servidor: {e}")


if __name__ == "__main__":
    apidb = ApiDB()
    # Puedes cambiar los puertos a no privilegiados si es necesario (ej. Syslog: 8514, NTP: 8123)
    start_server()
