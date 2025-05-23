DELIMITER //

CREATE PROCEDURE InsertarLog(
    IN p_HOSTNAME VARCHAR(50),
    IN p_codigo_sys INT,
    IN p_n_secuencia_syslog INT,
    IN p_fecha VARCHAR(50),                -- Recibe la fecha como cadena en formato "Nov 22 18:57:35.284"
    IN p_SUBSISTEMA VARCHAR(20),
    IN p_NIVEL INT,
    IN p_TIPO_DE_EVENTO VARCHAR(20),
    IN p_LOG TEXT
)
BEGIN
    DECLARE formatted_date DATETIME(3);    -- Variable para almacenar la fecha en formato MySQL
    DECLARE current_year INT;              -- Variable para almacenar el año actual

    -- Obtener el año actual
    SET current_year = YEAR(CURDATE());

    -- Convertir la fecha recibida al formato DATETIME(3)
    SET formatted_date = STR_TO_DATE(CONCAT(current_year, ' ', p_fecha), '%Y %b %d %H:%i:%s.%f');

    -- Inserción del log en la tabla Logs
    INSERT INTO Logs (HOSTNAME, codigo_sys, n_secuencia_syslog, DIA_HORA, SUBSISTEMA, NIVEL, TIPO_DE_EVENTO, LOG)
    VALUES (p_HOSTNAME, p_codigo_sys, p_n_secuencia_syslog, formatted_date, p_SUBSISTEMA, p_NIVEL, p_TIPO_DE_EVENTO, p_LOG);
END //

DELIMITER ;
