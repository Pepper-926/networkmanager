
-- Tabla Dispositivos
CREATE TABLE Dispositivos (
    HOSTNAME VARCHAR(15) NOT NULL PRIMARY KEY, -- Identificador único del dispositivo
    OS VARCHAR(10) NOT NULL,                  -- Anteriormente llamado TIPO, renombrado a OS
    SECRET VARCHAR(64) NOT NULL,              -- Contraseña secreta
    TIPO VARCHAR(20) NOT NULL                 -- Nueva columna, ahora no permite valores NULL
);


-- Tabla de interfaces
CREATE TABLE Interfaces (
    HOSTNAME VARCHAR(15) NOT NULL,
    IP VARCHAR(15),
    INTERFAZ VARCHAR(15) NOT NULL,
    TIPO_INTERFAZ VARCHAR(15) NOT NULL,
    PRIMARY KEY (HOSTNAME, INTERFAZ), -- Clave primaria compuesta
    FOREIGN KEY (HOSTNAME) REFERENCES Dispositivos (HOSTNAME)
);

-- Tabla de usuarios
CREATE TABLE Usuarios (
    HOSTNAME VARCHAR(15) NOT NULL,
    Usuario VARCHAR(15) NOT NULL,
    CONTRASENA VARCHAR(70) NOT NULL,
    PRIMARY KEY (HOSTNAME, Usuario), -- Clave primaria compuesta
    FOREIGN KEY (HOSTNAME) REFERENCES Dispositivos (HOSTNAME)
);

-- Tabla de historial de comandos
CREATE TABLE Historial (
    ID INT AUTO_INCREMENT PRIMARY KEY, -- Identificador único
    HOSTNAME VARCHAR(15) NOT NULL, -- Relación con dispositivos
    Usuario VARCHAR(15) NOT NULL, -- Usuario que ejecutó el comando
    COMANDO_PUESTO VARCHAR(40) NOT NULL,
    DIA_HORA DATETIME NOT NULL,
    FOREIGN KEY (HOSTNAME) REFERENCES Dispositivos (HOSTNAME)
);

-- Tabla de logs
CREATE TABLE Logs (
    HOSTNAME VARCHAR(15) NOT NULL,                   -- Relación con dispositivos
    codigo_sys INT NOT NULL,                         -- Código syslog
    n_secuencia_syslog INT NOT NULL,                 -- Número de secuencia del syslog
    DIA_HORA DATETIME(3) NOT NULL,                   -- Fecha y hora con milisegundos
    SUBSISTEMA VARCHAR(20) NOT NULL,                 -- Subsistema (como LINK, OSPF, etc.)
    NIVEL INT NOT NULL CHECK (NIVEL BETWEEN 0 AND 7),-- Nivel syslog (0 a 7)
    TIPO_DE_EVENTO VARCHAR(20) NOT NULL,             -- Tipo de evento (mnemonic)
    LOG TEXT NOT NULL,                               -- Mensaje del log
    PRIMARY KEY (HOSTNAME, n_secuencia_syslog),      -- Clave primaria compuesta
    FOREIGN KEY (HOSTNAME) REFERENCES Dispositivos (HOSTNAME),
    INDEX (HOSTNAME),                                -- Índice para búsquedas rápidas
    INDEX (DIA_HORA)                                 -- Índice para consultas por fecha
);

-- Tabla de directorio
CREATE TABLE Directorio (
    HOSTNAME VARCHAR(15) NOT NULL,
    DIRECTORIO VARCHAR(150) NOT NULL PRIMARY KEY,
    tipo VARCHAR(10),
    FOREIGN KEY (HOSTNAME) REFERENCES Dispositivos (HOSTNAME)
);

CREATE VIEW vwConexionNetmiko AS
SELECT 
    d.tipo AS device_type,
    i.ip AS host,
    u.Usuario AS username,
    u.CONTRASENA AS password,
    d.SECRET AS secret
FROM Dispositivos d
INNER JOIN Usuarios u ON u.HOSTNAME = d.HOSTNAME
INNER JOIN Interfaces i ON i.HOSTNAME = d.HOSTNAME
WHERE i.IP IS NOT NULL
ORDER BY d.HOSTNAME ASC;



CREATE OR REPLACE VIEW vwLogs AS
SELECT 
    HOSTNAME,
    codigo_sys,
    n_secuencia_syslog,
    DIA_HORA,
    SUBSISTEMA,
    NIVEL,
    TIPO_DE_EVENTO,
    LOG,
    CONCAT(
        HOSTNAME, ': <', codigo_sys, '>', n_secuencia_syslog, ': *', DIA_HORA, 
        ': %', SUBSISTEMA, '-', NIVEL, '-', TIPO_DE_EVENTO, ': ', LOG
    ) AS mensaje
FROM Logs;
