import pymysql
from extraccion_de_datos import *

class ApiDB:
    def __init__(self):
        self.host = '127.0.0.1'
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
        
    def insertar_log(self, addr,log):
        try:

            #Extraemos cada parte del mensaje syslog
            ip = addr[0]
            hostname = self.obtener_hostname(ip)
            codigo_syslog = extraer_syslog_codigo(log).replace('<','').replace('>','')
            secuencia = extraer_codigo_secuencia(log)
            fecha = extraer_fecha(log)
            subsistema, nivel, tipo_evento = extraer_partes_syslog(log)
            mensaje = extraer_mensaje_syslog(log)
            message = f"{addr[0]}: <{codigo_syslog}>{secuencia}: *{fecha}: %{subsistema}-{nivel}-{tipo_evento}: {mensaje}"
            hostname = self.obtener_hostname(ip)

            parameters = (hostname,codigo_syslog,secuencia,fecha,subsistema,nivel,tipo_evento,mensaje)

            #Conectamos a la base de datos e insertamos el log
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute(
            '''CALL InsertarLog(%s, %s, %s, %s, %s, %s, %s, %s);''',
            parameters
            )
            cursor.close()
            conn.commit()
            conn.close()  # Cierra la conexión antes de devolver el resultado

            with open("syslog_logs.txt", "a") as logfile:
                logfile.write(f"{addr}: {message}\n")


        except Exception as e:
            print('Error: ' ,e)
            cursor.close()
            conn.close() 
            return None


    def hosts_netmiko(self):
        try:
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute("SELECT * FROM vwConexionNetmiko")
            hosts = cursor.fetchall()  # "Recoge" el resultado en una tupla de diccionarios}
            cursor.close()
            conn.close()  # Cierra la conexión antes de devolver el resultado
            return hosts
        
        except Exception as e:
            print('Error: ' ,e)
            cursor.close()
            conn.close() 
            return None
        

    
if __name__ == '__main__':
    db = ApiDB()
    hostname = db.obtener_hostname('10.0.10.5')
    print(hostname)
