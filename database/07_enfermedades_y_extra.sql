-- =====================================================
-- ARCHIVO: 07_enfermedades_y_extra.sql
-- DESCRIPCION: Tabla de enfermedades predefinidas para
--              selector en la app + datos de ejemplo
-- ORDEN: Ejecutar DESPUES de 06_triggers_y_checks.sql
-- =====================================================

USE centro_salud;

-- =====================================================
-- TABLA: enfermedad (catálogo de enfermedades)
-- =====================================================
CREATE TABLE IF NOT EXISTS enfermedad (
    id_enfermedad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL UNIQUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Enfermedades predefinidas
INSERT INTO enfermedad (nombre) VALUES
('Hipertensión arterial'),
('Diabetes tipo 1'),
('Diabetes tipo 2'),
('Bronquitis aguda'),
('Asma bronquial'),
('Arritmia cardíaca'),
('Dermatitis alérgica'),
('Infección respiratoria aguda'),
('Gripe común'),
('COVID-19'),
('Neumonía'),
('Ansiedad generalizada'),
('Depresión'),
('Migraña'),
('Lumbalgia'),
('Gastritis crónica'),
('Infección urinaria'),
('Anemia ferropénica'),
('Hipotiroidismo'),
('Artritis reumatoide'),
('Obesidad'),
('Colesterol elevado'),
('Insuficiencia cardíaca'),
('Enfermedad pulmonar obstructiva crónica'),
('Cefalea tensional')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- =====================================================
-- MODIFICAR PROCEDURE sp_pacientes_por_diagnostico
-- Versión que busca también por enfermedad predefinida
-- =====================================================
DELIMITER $$

DROP PROCEDURE IF EXISTS sp_pacientes_por_diagnostico $$
CREATE PROCEDURE sp_pacientes_por_diagnostico(IN p_busqueda VARCHAR(100))
BEGIN
    IF p_busqueda IS NULL OR TRIM(p_busqueda) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar una enfermedad o palabra clave de diagnóstico.';
    END IF;

    SELECT DISTINCT *
    FROM vw_diagnosticos_pacientes
    WHERE diagnostico LIKE CONCAT('%', TRIM(p_busqueda), '%')
       OR paciente LIKE CONCAT('%', TRIM(p_busqueda), '%')
    ORDER BY fecha DESC, paciente;
END $$

DELIMITER ;
