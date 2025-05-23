import pymysql

class ApiDB:  #Clase que unicamente te conecta con la base de datos. Aqui van los datos de la base de datos
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'Gabriel'
        self.password = 'Pepper_926'
        self.db = 'Proyecto_redes'

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

    def buscar_hostname(self,hostname):
        """
        Se usa para asegurarnos que el hostname que deseamos
        insertar sea unico en la base de datos.

        Args:
            string hostname

        Returns:
            bool True o bool False
        """
        try:
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute('''select *
                           from dispositivos
                           where hostname = %s''', (hostname))
            host = cursor.fetchall()
            cursor.close()
            conn.close()  # Cierra la conexión antes de devolver el resultado
            if host == ():
                return True
            else:
                return False
        
        except Exception as e:
            print('Error: ' ,e)
            try:
                cursor.close()
                conn.close()
            except Exception as e:
                return 
            return None
        
    def registrar_dispositivo(self,cisco_device,interfaces):
        try:
            conn = self.get_db_connection()  # Realiza la conexion a la base de datos de admin con el socket
            cursor = conn.cursor()  # Crea un cursor para realizar querys
            # Consulta con parámetros para evitar inyección SQL
            cursor.execute('''insert into dispositivos (hostname,os,secret,tipo)
                           values (%s,'cisco_ios',%s,%s)''', (cisco_device['hostname'],cisco_device['secret'],cisco_device['tipo']))
            cursor.execute('''insert into usuarios (hostname,usuario,contraseña)
                values (%s,%s,%s)''', (cisco_device['hostname'],cisco_device['username'],cisco_device['password']))
            if cisco_device['tipo'] == 'router':
                for interfaz in interfaces:
                    cursor.execute('''insert into interfaces (hostname,ip,interfaz,tipo_interfaz)
                                   values (%s,%s,%s,'router')''',(cisco_device['hostname'],interfaz['IP-Address'],interfaz['Interface']))

            conn.commit()
            cursor.close()
            conn.close()  # Cierra la conexión antes de devolver el resultado

        except Exception as e:
            print('Error: ' ,e)
            try:
                cursor.close()
                conn.close()
            except Exception as e:
                return 
            return None
