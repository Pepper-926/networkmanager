class ExtraccionDeDatos:
    """
    Clase para procesar datos de interfaces de red y extraer información estructurada.
    """

    @staticmethod
    def extraccion_sh_ip_int_brief(interface_data):
        """
        Procesa un string de información de interfaces y devuelve una tupla de diccionarios
        con solo 'Interface' e 'IP-Address'.

        :param interface_data: Cadena de texto con la salida del comando "show ip interface brief"
        :return: Tupla de diccionarios con los datos filtrados.
        """
        # Dividir el string en líneas
        lines = interface_data.strip().split("\n")

        # Encabezados relevantes
        headers = ["Interface", "IP-Address"]
        interfaces = []

        # Procesar cada línea después del encabezado
        for line in lines[1:]:
            # Separar por espacios múltiples
            parts = line.split()

            # Crear un diccionario con solo Interface e IP-Address
            interface_dict = {
                headers[0]: parts[0],  # Interface
                headers[1]: parts[1]  # IP-Address
            }

            # Añadir el diccionario a la lista
            interfaces.append(interface_dict)

        return tuple(interfaces)
    
    @staticmethod
    def extraccion_hostname(hostname_data):
        """
        Extrae y devuelve el nombre del host de un string en el formato 'hostname <nombre>'.

        :param hostname_data: Cadena de texto con el comando "hostname <nombre>"
        :return: El nombre del host como string.
        """
        # Dividir el string por espacios
        parts = hostname_data.strip().split()

        # Validar que el formato sea correcto y devolver el segundo elemento
        if len(parts) == 2 and parts[0].lower() == "hostname":
            return parts[1]
        else:
            raise ValueError("El formato del string no es válido. Se esperaba 'hostname <nombre>'.")
        
    @staticmethod
    def tipo_dispositivo(route_data):
        """
        Determina si el dispositivo es un router o un switch basado en la cantidad de líneas
        del routing table.

        :param route_data: Cadena de texto con la salida de la tabla de enrutamiento
        :return: 'router' si tiene más de 7 líneas, 'switch' si tiene 7 o menos.
        """
        # Dividir en líneas y contar las que contienen datos de rutas (ignorar encabezados)
        route_lines = [line for line in route_data.strip().split("\n") if line.strip()]
        
        # Comprobar si hay más de 7 líneas
        return "router" if len(route_lines) > 7 else "switch"