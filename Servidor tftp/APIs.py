import pymysql

class ApiDB:
    def __init__(self):
        self.host = 'gabrielgarcia-926.ddns.net'
        self.user = 'Gabriel'
        self.password = 'Pepper_926'
        self.db = 'Proyecto_Redes'

    def get_db_connection(self):
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db,
                cursorclass=pymysql.cursors.DictCursor
            )
            return conn
        except pymysql.MySQLError as e:
            print(f"Error al conectar con la base de datos: {e}")
            return None

class ApiDBtftp(ApiDB):
    def __init__(self):
        super().__init__()

    def obtener_hostname(self, ip):
        """
        Obtiene el hostname de una ip

        Args:
            dirrecion_ip (str)

        Returns:
            str: Hostname.
            Si no hay coincidencia devuelve la misma ip
        """
        try:
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute('''SELECT HOSTNAME 
                           FROM interfaces
                           WHERE ip = %s''', (ip))
            hostname = cursor.fetchone()  # "Recoge" el resultado en un diccionario
            cursor.close()
            conn.close()  # Cierra la conexión antes de devolver el resultado
            if hostname is not None:
                return hostname['HOSTNAME']
            print(f"La ip {ip} no esta registrado en ningun dispositivo.")
            return ip
        
        except Exception as e:
            print('Error: ' ,e)
            cursor.close()
            conn.close() 
            return None
        
    def guardar_ruta(self, hostname, path, tipo):
        path = path.replace("\\", "/")
        """
        Intenta insertar la ruta de los runnings de los dispositivos
        en la base de datos. Si ya esta registrado no se inserta 
        y no generara un error

        Args:
            hostname (str)
            path (str)

        Returns:
            Nothing
        """
        try:
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute('''Insert into directorio (HOSTNAME, DIRECTORIO, TIPO)
                           values (%s,%s,%s)''', (hostname, path, tipo))
            conn.commit()
            cursor.close()
            conn.close()  # Cierra la conexión antes de devolver el resultado
            return
        
        except Exception as e:
            print('Error: ' ,e)
            cursor.close()
            conn.close() 
            return
    
if __name__ == '__main__':
    db = ApiDBtftp()
    hostname = db.obtener_hostname('10.0.10.5')
    print(hostname)