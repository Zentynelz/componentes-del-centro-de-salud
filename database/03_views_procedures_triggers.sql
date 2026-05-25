USE centro_salud;

CREATE OR REPLACE VIEW vw_pacientes_medicos AS
SELECT
    p.id_paciente,
    p.nombre AS paciente,
    p.direccion AS direccion_paciente,
    mp.nombre AS municipio_paciente,
    em.id_empleado AS id_medico,
    em.nombre AS medico,
    med.num_licencia,
    esp.nombre AS especialidad,
    tm.nombre AS tipo_medico
FROM paciente p
JOIN municipio mp ON p.id_municipio = mp.id_municipio
JOIN medico med ON p.id_empleado_medico = med.id_empleado
JOIN empleado em ON med.id_empleado = em.id_empleado
JOIN especialidad esp ON med.id_especialidad = esp.id_especialidad
JOIN tipo_medico tm ON med.id_tipo = tm.id_tipo;

CREATE OR REPLACE VIEW vw_medicos_info AS
SELECT
    e.id_empleado AS id_medico,
    e.nombre AS medico,
    e.direccion,
    mu.nombre AS municipio,
    m.num_licencia,
    tm.nombre AS tipo_medico,
    esp.nombre AS especialidad
FROM medico m
JOIN empleado e ON m.id_empleado = e.id_empleado
JOIN municipio mu ON e.id_municipio = mu.id_municipio
JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad;

CREATE OR REPLACE VIEW vw_diagnosticos_pacientes AS
SELECT
    d.id_diagnostico,
    d.fecha,
    d.descripcion AS diagnostico,
    p.id_paciente,
    p.nombre AS paciente,
    p.direccion AS direccion_paciente,
    mp.nombre AS municipio_paciente,
    em.id_empleado AS id_medico,
    em.nombre AS medico,
    esp.nombre AS especialidad
FROM diagnostico d
JOIN paciente p ON d.id_paciente = p.id_paciente
JOIN municipio mp ON p.id_municipio = mp.id_municipio
JOIN medico med ON p.id_empleado_medico = med.id_empleado
JOIN empleado em ON med.id_empleado = em.id_empleado
JOIN especialidad esp ON med.id_especialidad = esp.id_especialidad;

CREATE OR REPLACE VIEW vw_vacaciones_medicos AS
SELECT
    v.id_vacacion,
    v.fecha_inicio,
    v.fecha_fin,
    e.id_empleado AS id_medico,
    e.nombre AS medico,
    esp.nombre AS especialidad,
    CASE
        WHEN CURDATE() > v.fecha_fin THEN 'Disfrutadas'
        WHEN CURDATE() BETWEEN v.fecha_inicio AND v.fecha_fin THEN 'En curso'
        ELSE 'Planeadas'
    END AS estado_vacaciones
FROM vacaciones v
JOIN medico m ON v.id_empleado = m.id_empleado
JOIN empleado e ON m.id_empleado = e.id_empleado
JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad;

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_pacientes_por_especialidad $$
CREATE PROCEDURE sp_pacientes_por_especialidad(IN p_especialidad VARCHAR(100))
BEGIN
    SELECT *
    FROM vw_pacientes_medicos
    WHERE especialidad = p_especialidad
    ORDER BY medico, paciente;
END $$

DROP PROCEDURE IF EXISTS sp_medicos_disponibles_por_especialidad $$
CREATE PROCEDURE sp_medicos_disponibles_por_especialidad(IN p_especialidad VARCHAR(100))
BEGIN
    SELECT
        mi.id_medico,
        mi.medico,
        mi.num_licencia,
        mi.tipo_medico,
        mi.especialidad,
        GROUP_CONCAT(CONCAT(h.dia_semana, ' ', TIME_FORMAT(h.hora_inicio, '%H:%i'), '-', TIME_FORMAT(h.hora_fin, '%H:%i'))
                     ORDER BY FIELD(h.dia_semana, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
                     SEPARATOR ' | ') AS horarios
    FROM vw_medicos_info mi
    LEFT JOIN horario h ON mi.id_medico = h.id_empleado_medico
    WHERE mi.especialidad = p_especialidad
      AND NOT EXISTS (
          SELECT 1
          FROM vacaciones v
          WHERE v.id_empleado = mi.id_medico
            AND CURDATE() BETWEEN v.fecha_inicio AND v.fecha_fin
      )
      AND (
          mi.tipo_medico <> 'Sustituto'
          OR EXISTS (
              SELECT 1
              FROM periodo_sustituto ps
              WHERE ps.id_empleado_medico = mi.id_medico
                AND ps.fecha_ingreso = (
                    SELECT MAX(ps2.fecha_ingreso)
                    FROM periodo_sustituto ps2
                    WHERE ps2.id_empleado_medico = mi.id_medico
                )
                AND (ps.fecha_retiro IS NULL OR ps.fecha_ingreso > ps.fecha_retiro OR CURDATE() <= ps.fecha_retiro)
          )
      )
    GROUP BY mi.id_medico, mi.medico, mi.num_licencia, mi.tipo_medico, mi.especialidad
    ORDER BY mi.medico;
END $$

DROP PROCEDURE IF EXISTS sp_pacientes_por_diagnostico $$
CREATE PROCEDURE sp_pacientes_por_diagnostico(IN p_busqueda VARCHAR(100))
BEGIN
    SELECT *
    FROM vw_diagnosticos_pacientes
    WHERE diagnostico LIKE CONCAT('%', p_busqueda, '%')
    ORDER BY fecha DESC, paciente;
END $$

DROP PROCEDURE IF EXISTS sp_vacaciones_medicos_intervalo $$
CREATE PROCEDURE sp_vacaciones_medicos_intervalo(IN p_fecha_inicio DATE, IN p_fecha_fin DATE)
BEGIN
    SELECT *
    FROM vw_vacaciones_medicos
    WHERE fecha_inicio <= p_fecha_fin
      AND fecha_fin >= p_fecha_inicio
    ORDER BY fecha_inicio, medico;
END $$

DELIMITER ;
