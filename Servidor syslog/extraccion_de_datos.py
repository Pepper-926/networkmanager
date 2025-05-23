import re

def extraer_syslog_codigo(log_message):
    """
    Extrae el código syslog (como <187>) de un mensaje de log.

    Args:
        log_message (str): El mensaje de log completo.

    Returns:
        str: El código syslog extraído (por ejemplo, <187>).
    """
    # Expresión regular para buscar el código syslog en el formato <###>
    patron = r"<\d+>"
    match = re.search(patron, log_message)
    
    if match:
        return match.group(0)
    else:
        return "Código syslog no encontrado"

def extraer_codigo_secuencia(log_message):
    """
    Extrae el código de secuencia de un mensaje syslog.

    Args:
        log_message (str): Mensaje de syslog completo.

    Returns:
        str: El código de secuencia extraído.
    """
    # Expresión regular para buscar el código de secuencia
    patron = r"<\d+>(\d+):"
    match = re.search(patron, log_message)
    
    if match:
        return match.group(1)  # Devuelve el código de secuencia capturado
    else:
        return "Código de secuencia no encontrado"

def extraer_fecha(log_message):
    """
    Extrae la fecha de un mensaje de log.

    Args:
        log_message (str): Mensaje de log en formato de texto.

    Returns:
        str: Fecha extraída del mensaje de log, en formato "Nov 22 18:12:09.197".
    """
    # Expresión regular para buscar la fecha con o sin el asterisco inicial
    patron_fecha = r"\*?\w{3} \d{1,2} \d{2}:\d{2}:\d{2}\.\d{3}"
    match = re.search(patron_fecha, log_message)
    
    if match:
        # Quitar el asterisco inicial si está presente
        return match.group(0).lstrip('*')
    else:
        print("Fecha no encontrada en el siguiente log: " ,log_message)
        return

def extraer_partes_syslog(log_message):
    """
    Extrae el subsistema, severidad y mnemonics de un mensaje syslog.

    Args:
        log_message (str): Mensaje syslog completo.

    Returns:
        tuple: Una tupla con tres elementos (subsystem, severity, mnemonic).
    """
    # Expresión regular para extraer %SUBSYSTEM-SEVERITY-MNEMONIC:
    patron = r"%(\w+)-(\d+)-(\w+):"
    match = re.search(patron, log_message)
    
    if match:
        subsystem = match.group(1)  # LINK
        severity = match.group(2)  # 3
        mnemonic = match.group(3)  # UPDOWN
        return subsystem, severity, mnemonic
    else:
        return None, None, None
    
def extraer_mensaje_syslog(log_message):
    """
    Extrae el mensaje detallado después de %SUBSYSTEM-SEVERITY-MNEMONIC: de un mensaje syslog.

    Args:
        log_message (str): Mensaje syslog completo.

    Returns:
        str: El mensaje detallado extraído.
    """
    # Expresión regular para capturar el texto después de %DUAL-6-NBRINFO:
    patron = r"%\w+-\d+-\w+: (.+)"
    match = re.search(patron, log_message)
    
    if match:
        return match.group(1)  # Captura el mensaje después del patrón
    else:
        return "Mensaje no encontrado"