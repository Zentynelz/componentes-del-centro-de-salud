-- Fix encoding in enfermedad table
UPDATE enfermedad SET nombre = 'Anemia ferropénica' WHERE id_enfermedad = 18;
UPDATE enfermedad SET nombre = 'Arritmia cardíaca' WHERE id_enfermedad = 6;
UPDATE enfermedad SET nombre = 'Artritis reumatoide' WHERE id_enfermedad = 20;
UPDATE enfermedad SET nombre = 'Colesterol elevado' WHERE id_enfermedad = 22;
UPDATE enfermedad SET nombre = 'Depresión' WHERE id_enfermedad = 13;
UPDATE enfermedad SET nombre = 'Dermatitis alérgica' WHERE id_enfermedad = 7;
UPDATE enfermedad SET nombre = 'Enfermedad pulmonar obstructiva crónica' WHERE id_enfermedad = 24;
UPDATE enfermedad SET nombre = 'Gastritis crónica' WHERE id_enfermedad = 16;
UPDATE enfermedad SET nombre = 'Gripe común' WHERE id_enfermedad = 9;
UPDATE enfermedad SET nombre = 'Hipertensión arterial' WHERE id_enfermedad = 1;
UPDATE enfermedad SET nombre = 'Infección respiratoria aguda' WHERE id_enfermedad = 8;
UPDATE enfermedad SET nombre = 'Infección urinaria' WHERE id_enfermedad = 17;
UPDATE enfermedad SET nombre = 'Insuficiencia cardíaca' WHERE id_enfermedad = 23;
UPDATE enfermedad SET nombre = 'Migraña' WHERE id_enfermedad = 14;
UPDATE enfermedad SET nombre = 'Neumonía' WHERE id_enfermedad = 11;
UPDATE enfermedad SET nombre = 'Obesidad' WHERE id_enfermedad = 21;

-- Add id_enfermedad FK to diagnostico
ALTER TABLE diagnostico
ADD COLUMN id_enfermedad INT DEFAULT NULL AFTER id_usuario_creacion,
ADD CONSTRAINT fk_diagnostico_enfermedad
    FOREIGN KEY (id_enfermedad) REFERENCES enfermedad(id_enfermedad)
    ON DELETE SET NULL;

-- Update existing diagnosticos with disease from descripcion
UPDATE diagnostico d
JOIN enfermedad e ON d.descripcion LIKE CONCAT('%', e.nombre, '%')
SET d.id_enfermedad = e.id_enfermedad;

-- Upgrade the view to include enfermedad name
DROP VIEW IF EXISTS vw_diagnosticos_pacientes;
CREATE VIEW vw_diagnosticos_pacientes AS
SELECT
    d.id_diagnostico,
    d.fecha,
    d.descripcion,
    COALESCE(e.nombre, 'Sin enfermedad') AS enfermedad,
    d.id_paciente,
    p.nombre AS paciente,
    p.direccion AS direccion_paciente,
    m.nombre AS municipio_paciente,
    em.id_empleado AS id_medico,
    em.nombre AS medico,
    esp.nombre AS especialidad
FROM diagnostico d
JOIN paciente p ON d.id_paciente = p.id_paciente
LEFT JOIN municipio m ON p.id_municipio = m.id_municipio
LEFT JOIN empleado em ON p.id_empleado_medico = em.id_empleado
LEFT JOIN medico me ON em.id_empleado = me.id_empleado
LEFT JOIN especialidad esp ON me.id_especialidad = esp.id_especialidad
LEFT JOIN enfermedad e ON d.id_enfermedad = e.id_enfermedad;

-- Upgrade the procedure to use enfermedad FK
DROP PROCEDURE IF EXISTS sp_pacientes_por_diagnostico;
DELIMITER $$
CREATE PROCEDURE sp_pacientes_por_diagnostico(IN p_enfermedad VARCHAR(150))
BEGIN
    IF p_enfermedad IS NULL OR TRIM(p_enfermedad) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar una enfermedad para la busqueda.';
    END IF;

    SELECT *
    FROM vw_diagnosticos_pacientes
    WHERE enfermedad LIKE CONCAT('%', TRIM(p_enfermedad), '%')
    ORDER BY fecha DESC, paciente;
END $$
DELIMITER ;
