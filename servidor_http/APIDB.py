import pymysql
import os
from datetime import datetime

class ApiDB:
    def __init__(self):
        self.host = os.environ.get('DB_HOST', 'localhost')
        self.user = os.environ.get('DB_USER', 'Gabriel')
        self.password = os.environ.get('DB_PASS', 'Pepper_926')
        self.db = os.environ.get('DB_NAME', 'Proyecto_Redes')

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

    def convertir_datetime(self, fecha_iso):
        try:
            fecha = datetime.strptime(fecha_iso, "%Y-%m-%dT%H:%M")
            return fecha.strftime("%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("El formato de la fecha debe ser 'YYYY-MM-DDTHH:MM'.")

    def obtener_hostname(self, ip):
        conn = self.get_db_connection()
        cursor = None
        try:
            if not conn:
                return None
            cursor = conn.cursor()
            cursor.execute("SELECT HOSTNAME FROM interfaces WHERE ip = %s", (ip,))
            hostname = cursor.fetchone()
            if hostname:
                return hostname['HOSTNAME']
            print(f"La IP {ip} no está registrada.")
            return ip
        except Exception as e:
            print('Error:', e)
            return None
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def filtrar_logs(self, filtros):
        query = "SELECT MENSAJE FROM VWLOGS WHERE 1=1"
        parameters = []

        if filtros['hostname']:
            parameters.append(filtros['hostname'])
            query += " AND HOSTNAME = %s"
        if filtros['codigo_sys']:
            parameters.append(filtros['codigo_sys'])
            query += " AND CODIGO_SYS = %s"
        if filtros['n_secuencia']:
            parameters.append(filtros['n_secuencia'])
            query += " AND N_SECUENCIA_SYSLOG = %s"
        if filtros['fecha_inicio']:
            fecha_inicio = self.convertir_datetime(filtros['fecha_inicio'])
            parameters.append(fecha_inicio)
            query += " AND DIA_HORA >= %s"
        if filtros['fecha_fin']:
            fecha_fin = self.convertir_datetime(filtros['fecha_fin'])
            parameters.append(fecha_fin)
            query += " AND DIA_HORA <= %s"
        if filtros['subsistema']:
            parameters.append(filtros['subsistema'])
            query += " AND SUBSISTEMA = %s"
        if filtros['nivel']:
            parameters.append(filtros['nivel'])
            query += " AND NIVEL = %s"
        if filtros['tipo_evento']:
            parameters.append(filtros['tipo_evento'])
            query += " AND TIPO_DE_EVENTO = %s"
        query += " ORDER BY DIA_HORA ASC;"

        conn = self.get_db_connection()
        cursor = None
        try:
            if not conn:
                return []
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            logs = cursor.fetchall()
            return logs
        except Exception as e:
            print('Error:', e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def obtener_opciones_logs(self):
        conn = self.get_db_connection()
        cursor = None
        try:
            if not conn:
                return []
            opciones = []
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT HOSTNAME FROM VWLOGS;")
            hostnames = cursor.fetchall()
            opciones.append(tuple(hostnames))

            cursor.execute("SELECT DISTINCT SUBSISTEMA FROM VWLOGS;")
            subsistemas = cursor.fetchall()
            opciones.append(tuple(subsistemas))

            cursor.execute("SELECT DISTINCT TIPO_DE_EVENTO FROM VWLOGS;")
            eventos = cursor.fetchall()
            opciones.append(tuple(eventos))

            return tuple(opciones)
        except Exception as e:
            print('Error:', e)
            return []
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

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
