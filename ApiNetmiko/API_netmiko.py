from netmiko import ConnectHandler
from API_DB import ApiDB
from clase_filtro import ExtraccionDeDatos

db_conn = ApiDB()

class ApiNetmikoGabo:
    def agregar_dispositivo(self,host,username,password,secret): 
        extraccion = ExtraccionDeDatos()
        # Configuración del dispositivo Cisco
        cisco_device = {
            'device_type': 'cisco_ios',  # Tipo de dispositivo
            'host': host,       # Dirección IP del router
            'username': username,         # Usuario
            'password': password,      # Contraseña
            'secret': secret,  # Contraseña de modo enable (si aplica)
        }

        try:
            # Conectar al dispositivo
            print("Conectando al dispositivo...")
            connection = ConnectHandler(**cisco_device)
            print('Conexion exitosa. Accediendo al modo privilegiado.')

            # Entrar en modo enable (si es necesario)
            if 'secret' in cisco_device and cisco_device['secret']:
                connection.enable()

            print('Acceso al modo privilegiado exitoso. Obteniendo hostname.')

            sh_runn_hostname = connection.send_command('show running-config | include hostname')
            hostname = extraccion.extraccion_hostname(sh_runn_hostname)

            ip_route = connection.send_command('show ip route')
            tipo_dispositivo = extraccion.tipo_dispositivo(ip_route)

            while True:
                dec = input(f'¿{hostname} ({tipo_dispositivo}) es el nombre y tipo de dispositivo que quieres agregar?[Y/N]: ')
                if dec.upper() == 'Y':
                    if db_conn.buscar_hostname(hostname):
                        cisco_device['hostname'] = hostname
                        cisco_device['tipo'] = tipo_dispositivo
                        break
                    else:
                        print('Ya hay un dispositivo con ese hostname en la base de datos.')
                        return

                if dec.upper() == 'N':
                    print('Cancelando registro de nuevo dispositivo.\nCompruebe que el dispositivo si tenga el hostname deseado y que la ip sea la correcta.')
                    return
                else:
                    print('Porfavor de una respuesta valida.')

            interfaces = connection.send_command('show ip int brief')

            interfaces = extraccion.extraccion_sh_ip_int_brief(interfaces)
            print('Mostrando datos de las interfaces del dispositivo:\n')
            print('Interfaz    IP')
            for interfaz in interfaces:
                print(interfaz['Interface'],interfaz['IP-Address'])

            while True:
                dec = input('¿Son esos datos correctos? [Y/N]: ')
                if dec.upper() == 'Y':
                    print('Registrando dispositivo en la base de datos. Puede tomar algunos segundos.')
                    db_conn.registrar_dispositivo(cisco_device,interfaces)
                    print('Dispositivo registrado con exito.')
                    break
                if dec.upper() == 'N':
                    print('Cancelando registro de nuevo dispositivo.\nEs posible que la direccion ip no sea la correcta.')
                    break
                else:
                    print('Porfavor de una respuesta valida.')

            connection.disconnect()
            print("\nConexión cerrada.")

        except Exception as e:
            print(f"Error: {e}")
            print('Volviendo al menu.')
            try:
                connection.disconnect()
                return
            except Exception:
                return

    def obtener_backup():
        pass
