import pymysql
from datetime import datetime


'''
Aqui van las clases de la api a la base de datos
'''

class ApiDB:  #Clase que unicamente te conecta con la base de datos
    def __init__(self):
        self.host = 'localhost'
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

class ApiDBGabriel(ApiDB):
    def __init__(self):
        super().__init__()

    def convertir_datetime(self,fecha_iso):
        """
    Convierte una fecha en formato ISO 8601 (YYYY-MM-DDTHH:MM)
    al formato DATETIME de MySQL (YYYY-MM-DD HH:MM:SS).

    Args:
        fecha_iso (str): Fecha en formato ISO 8601 (YYYY-MM-DDTHH:MM).

    Returns:
        str: Fecha en formato MySQL DATETIME (YYYY-MM-DD HH:MM:SS).
    """
        try:
            # Parsear la fecha en formato ISO 8601
            fecha = datetime.strptime(fecha_iso, "%Y-%m-%dT%H:%M")
            # Formatear al formato MySQL
            return fecha.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("El formato de la fecha debe ser 'YYYY-MM-DDTHH:MM'.")

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
        
    def filtrar_logs(self,filtros):
        """
        Construye el query para obtener los logs segun
        los filtros mandados desde el frontend y devuelve una tupla
        de diccionarios con los mensajes logs

        Args:
            filtos (diccionario)

        Returns:
            tupla de diccionarios: logs.
        """
        # Construimos el query
        query = 'SELECT MENSAJE FROM VWLOGS WHERE 1=1'
        parameters = []

        if filtros['hostname'] is not None:
            parameters.append(filtros['hostname'])
            query += " AND HOSTNAME = %s"
        if filtros['codigo_sys'] != '':
            parameters.append(filtros['codigo_sys'])
            query += " AND CODIGO_SYS = %s"
        if filtros['n_secuencia'] != '':
            parameters.append(filtros['n_secuencia'])
            query += " AND N_SECUENCIA_SYSLOG = %s"
        if filtros['fecha_inicio'] != '':
            # Transformamos la fecha en un formato que entienda MySQL
            fecha_inicio = self.convertir_datetime(filtros['fecha_inicio'])
            parameters.append(fecha_inicio)
            query += " AND DIA_HORA >= %s"
        if filtros['fecha_fin'] != '':
            fecha_fin = self.convertir_datetime(filtros['fecha_fin'])
            parameters.append(fecha_fin)
            query += " AND DIA_HORA <= %s"
        if filtros['subsistema'] is not None:
            parameters.append(filtros['subsistema'])
            query += " AND SUBSISTEMA = %s"
        if filtros['nivel'] is not None:
            parameters.append(filtros['nivel'])
            query += " AND NIVEL = %s"
        if filtros['tipo_evento'] is not None:
            parameters.append(filtros['tipo_evento'])
            query += " AND TIPO_DE_EVENTO = %s"
        query += " ORDER BY DIA_HORA ASC;"

        try:
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            logs = cursor.fetchall()
            cursor.close()
            conn.close()
            return logs
        except Exception as e:
            print('error: ', e)
            cursor.close()
            conn.close()
            return None

    def obtener_opciones_logs(self):
        """
        Obtiene todas las opciones disponibles en base
        a los logs registrados. Por ejemplo. si no hay ningun
        log del subsistema NBRINFO en los registros logs, el formulario 
        no le dara la opcion de buscar logs enviados por el subsistema NBRINFO
        porque no hay.

        Args:
            None

        Returns:
            tupla de tuplas de diccionarios: opciones.
        """
        try:
            opciones = []
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            cursor.execute('''SELECT DISTINCT HOSTNAME
                           FROM VWLOGS;
                            ''')
            hostnames = cursor.fetchall()
            opciones.append(tuple(hostnames))

            cursor.execute('''SELECT DISTINCT SUBSISTEMA
                           FROM VWLOGS;
                            ''')
            subsistemas = cursor.fetchall()
            opciones.append(tuple(subsistemas))

            cursor.execute('''SELECT DISTINCT TIPO_DE_EVENTO
                           FROM VWLOGS;
                            ''')
            eventos = cursor.fetchall()
            opciones.append(tuple(eventos))

            cursor.close()
            conn.close()
            return tuple(opciones)
        
        except Exception as e:
            print('Error: ' ,e)
            cursor.close()
            conn.close() 
            return None

        
class ApiDBMata(ApiDB):
    def __init__(self):
        super().__init__()




class ApiDBGaLa(ApiDB):
    def __init__(self):
        super().__init__()



class ApiDBKaren(ApiDB):
    def __init__(self):
        super().__init__()





    
if __name__ == '__main__':
    db = ApiDBGabriel()
    filtros = {'hostname': None, 'codigo_sys': '', 'n_secuencia': '', 'fecha_inicio': '', 'fecha_fin': '', 'subsistema': None, 'nivel': None, 'tipo_evento': None}
    logs = db.filtrar_logs(filtros)
    for log in logs:
        print(log)