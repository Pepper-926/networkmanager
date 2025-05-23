import socket
import os
from APIs import ApiDBtftp
from datetime import datetime



def handle_wrq(sock, client_addr, directory):
    """
    Maneja una solicitud de escritura (WRQ) desde un cliente TFTP.
    Crea una carpeta con el nombre de la IP del cliente y guarda el archivo en esa carpeta.
    """
    directorio_virtual = '/runnings/'
    try:
        ip_address = client_addr[0]

        # Obtenemos el hostname de la IP si está registrado en la base de datos
        hostname = apidb.obtener_hostname(ip_address)

        client_directory = os.path.join(directory, hostname)
        os.makedirs(client_directory, exist_ok=True)
        print(f"Carpeta creada o existente: {client_directory}")

        # Generamos el directorio virtual para el servidor FTP
        directorio_virtual_nuevo = directorio_virtual + hostname
        print(f'Directorio virtual generado: {directorio_virtual_nuevo}')  # Asegurar que siempre se imprima

        # Obtener la fecha y hora actual para incluirla en el nombre del archivo
        fecha_actual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Crear el nombre del archivo dentro de la carpeta
        save_path = os.path.join(client_directory, f"{hostname}_{fecha_actual}.txt")
        print(f"Guardando archivo como: {save_path}")

        # Intentar guardar la ruta del dispositivo en la base de datos en caso de que sea un dispositivo nuevo
        apidb.guardar_ruta(hostname, client_directory,'real')
        apidb.guardar_ruta(hostname, directorio_virtual_nuevo,'virtual')

        # Confirmar la solicitud con un ACK inicial (bloque 0)
        ack = b'\x00\x04\x00\x00'  # Opcode 4 (ACK) + Block Number 0
        sock.sendto(ack, client_addr)
        print(f"Solicitud de escritura aceptada de {ip_address}")

        # Abrir el archivo en modo escritura
        with open(save_path, 'wb') as f:
            block_number = 1
            while True:
                # Recibir datos del cliente
                data, addr = sock.recvfrom(516)
                if addr != client_addr:
                    print(f"Paquete ignorado de {addr}, esperando de {client_addr}")
                    continue

                opcode = int.from_bytes(data[:2], 'big')
                received_block = int.from_bytes(data[2:4], 'big')

                # Verificar si es un paquete DATA válido
                if opcode == 3 and received_block == block_number:
                    f.write(data[4:])  # Escribir datos en el archivo
                    print(f"Recibido bloque {block_number} ({len(data[4:])} bytes)")

                    # Enviar ACK para este bloque
                    ack = b'\x00\x04' + block_number.to_bytes(2, 'big')
                    sock.sendto(ack, client_addr)

                    # Si el bloque tiene menos de 512 bytes, es el último
                    if len(data[4:]) < 512:
                        print(f"Transferencia completada para {save_path}")
                        break

                    block_number += 1
                else:
                    print(f"Error: Paquete inesperado, Opcode: {opcode}, Bloque: {received_block}")
                    break

        # Imprimir nuevamente después del bucle, para verificar el directorio generado
        print(f"Directorio virtual generado final: {directorio_virtual_nuevo}")

    except Exception as e:
        print(f"Error manejando WRQ: {e}")
        send_error(sock, client_addr, 0, "Error handling write request")

def send_error(sock, client_addr, error_code, error_msg):
    """
    Envía un paquete de error al cliente TFTP.
    """
    packet = b'\x00\x05' + error_code.to_bytes(2, 'big') + error_msg.encode() + b'\x00'
    sock.sendto(packet, client_addr)

def start_tftp_server(host='0.0.0.0', port=69, directory='.'):
    """
    Inicia un servidor TFTP básico.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((host, port))
        print(f"Servidor TFTP iniciado en {host}:{port}, recibiendo archivos en {os.path.abspath(directory)}")

        while True:
            # Recibir solicitudes
            data, client_addr = sock.recvfrom(1024)
            opcode = int.from_bytes(data[:2], 'big')

            if opcode == 2:  # WRQ (Write Request)
                filename = data[2:].split(b'\x00')[0].decode()
                print(f"Solicitud de escritura (WRQ) recibida: {filename} desde {client_addr}")
                handle_wrq(sock, client_addr, directory)
            else:
                print(f"Solicitud no soportada: Opcode {opcode}")
                send_error(sock, client_addr, 4, "Operation not supported")
    except PermissionError:
        print("Error: Necesitas permisos de administrador para usar el puerto 69.")
    except Exception as e:
        print(f"Error en el servidor TFTP: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    # Cambia el directorio si deseas guardar los archivos en otro lugar
    apidb = ApiDBtftp()
    start_tftp_server(directory='C:/Users/gabri/OneDrive/Escritorio/Universidad/Semestre III/Redes II/Proyecto final/Codigos/Servidor tftp/tftp_files')

