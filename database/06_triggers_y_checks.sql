-- =====================================================
-- ARCHIVO: 06_triggers_y_checks.sql
-- DESCRIPCION: Tabla de auditoría, CHECK constraints y
--              triggers completos del centro de salud
-- ORDEN: Ejecutar DESPUES de 01_schema.sql, 02_seed.sql
--        y 03_views_procedures_triggers.sql
-- =====================================================

USE centro_salud;

-- =====================================================
-- 1. TABLA DE AUDITORIA
-- =====================================================
CREATE TABLE IF NOT EXISTS auditoria (
    id_auditoria INT AUTO_INCREMENT PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    operacion VARCHAR(20) NOT NULL,
    descripcion VARCHAR(255),
    fecha_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =====================================================
-- 2. CHECK CONSTRAINTS ADICIONALES (calidad de datos)
-- =====================================================

-- Validar que nombres no sean demasiado cortos
ALTER TABLE empleado
ADD CONSTRAINT chk_empleado_nombre
CHECK (CHAR_LENGTH(TRIM(nombre)) >= 3);

ALTER TABLE empleado
ADD CONSTRAINT chk_empleado_direccion
CHECK (CHAR_LENGTH(TRIM(direccion)) >= 5);

ALTER TABLE paciente
ADD CONSTRAINT chk_paciente_nombre
CHECK (CHAR_LENGTH(TRIM(nombre)) >= 3);

ALTER TABLE paciente
ADD CONSTRAINT chk_paciente_direccion
CHECK (CHAR_LENGTH(TRIM(direccion)) >= 5);

ALTER TABLE diagnostico
ADD CONSTRAINT chk_diagnostico_descripcion
CHECK (CHAR_LENGTH(TRIM(descripcion)) >= 5);

-- Validar formato de teléfonos (solo números, espacios, + y -)
ALTER TABLE telefono_empleado
ADD CONSTRAINT chk_tel_empleado_formato
CHECK (telefono REGEXP '^[0-9+ -]{7,20}$');

ALTER TABLE telefono_paciente
ADD CONSTRAINT chk_tel_paciente_formato
CHECK (telefono REGEXP '^[0-9+ -]{7,20}$');

-- =====================================================
-- 3. TRIGGERS
-- =====================================================

-- =====================================================
-- 3.1 TRIGGERS DE HORARIO
-- Evitan horarios traslapados para el mismo médico y día
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_horario_no_traslape_bi $$
CREATE TRIGGER trg_horario_no_traslape_bi
BEFORE INSERT ON horario
FOR EACH ROW
BEGIN
    IF NEW.hora_fin <= NEW.hora_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La hora de fin debe ser mayor que la hora de inicio.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM horario h
        WHERE h.id_empleado_medico = NEW.id_empleado_medico
          AND h.dia_semana = NEW.dia_semana
          AND NEW.hora_inicio < h.hora_fin
          AND NEW.hora_fin > h.hora_inicio
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El horario se traslapa con otro horario del mismo médico.';
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_horario_no_traslape_bu $$
CREATE TRIGGER trg_horario_no_traslape_bu
BEFORE UPDATE ON horario
FOR EACH ROW
BEGIN
    IF NEW.hora_fin <= NEW.hora_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La hora de fin debe ser mayor que la hora de inicio.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM horario h
        WHERE h.id_empleado_medico = NEW.id_empleado_medico
          AND h.dia_semana = NEW.dia_semana
          AND h.id_horario <> NEW.id_horario
          AND NEW.hora_inicio < h.hora_fin
          AND NEW.hora_fin > h.hora_inicio
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El horario actualizado se traslapa con otro horario del mismo médico.';
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.2 TRIGGERS DE VACACIONES
-- Evitan periodos vacacionales cruzados para el mismo empleado
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_vacaciones_no_traslape_bi $$
CREATE TRIGGER trg_vacaciones_no_traslape_bi
BEFORE INSERT ON vacaciones
FOR EACH ROW
BEGIN
    IF NEW.fecha_fin < NEW.fecha_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha fin de vacaciones no puede ser menor que la fecha inicio.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM vacaciones v
        WHERE v.id_empleado = NEW.id_empleado
          AND NEW.fecha_inicio <= v.fecha_fin
          AND NEW.fecha_fin >= v.fecha_inicio
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El empleado ya tiene vacaciones registradas en ese intervalo.';
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_vacaciones_no_traslape_bu $$
CREATE TRIGGER trg_vacaciones_no_traslape_bu
BEFORE UPDATE ON vacaciones
FOR EACH ROW
BEGIN
    IF NEW.fecha_fin < NEW.fecha_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha fin de vacaciones no puede ser menor que la fecha inicio.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM vacaciones v
        WHERE v.id_empleado = NEW.id_empleado
          AND v.id_vacacion <> NEW.id_vacacion
          AND NEW.fecha_inicio <= v.fecha_fin
          AND NEW.fecha_fin >= v.fecha_inicio
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El empleado ya tiene vacaciones registradas en ese intervalo.';
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.3 TRIGGERS DE PERIODOS DE SUSTITUCION
-- Validan que solo médicos sustitutos tengan periodos
-- y que no se crucen entre sí
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_periodo_sustituto_valida_bi $$
CREATE TRIGGER trg_periodo_sustituto_valida_bi
BEFORE INSERT ON periodo_sustituto
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM medico m
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        WHERE m.id_empleado = NEW.id_empleado_medico
          AND tm.nombre = 'Sustituto'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Solo los médicos de tipo Sustituto pueden tener periodos de sustitución.';
    END IF;

    IF NEW.fecha_retiro IS NOT NULL AND NEW.fecha_retiro < NEW.fecha_ingreso THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de retiro no puede ser menor que la fecha de ingreso.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM periodo_sustituto ps
        WHERE ps.id_empleado_medico = NEW.id_empleado_medico
          AND NEW.fecha_ingreso <= COALESCE(ps.fecha_retiro, '9999-12-31')
          AND COALESCE(NEW.fecha_retiro, '9999-12-31') >= ps.fecha_ingreso
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El periodo de sustitución se cruza con otro periodo existente.';
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_periodo_sustituto_valida_bu $$
CREATE TRIGGER trg_periodo_sustituto_valida_bu
BEFORE UPDATE ON periodo_sustituto
FOR EACH ROW
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM medico m
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        WHERE m.id_empleado = NEW.id_empleado_medico
          AND tm.nombre = 'Sustituto'
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Solo los médicos de tipo Sustituto pueden tener periodos de sustitución.';
    END IF;

    IF NEW.fecha_retiro IS NOT NULL AND NEW.fecha_retiro < NEW.fecha_ingreso THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de retiro no puede ser menor que la fecha de ingreso.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM periodo_sustituto ps
        WHERE ps.id_empleado_medico = NEW.id_empleado_medico
          AND ps.id_periodo <> NEW.id_periodo
          AND NEW.fecha_ingreso <= COALESCE(ps.fecha_retiro, '9999-12-31')
          AND COALESCE(NEW.fecha_retiro, '9999-12-31') >= ps.fecha_ingreso
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El periodo de sustitución actualizado se cruza con otro periodo existente.';
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.4 TRIGGERS DE DIAGNOSTICO
-- Evitan diagnósticos con fecha futura
-- o descripción insuficiente
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_diagnostico_valida_bi $$
CREATE TRIGGER trg_diagnostico_valida_bi
BEFORE INSERT ON diagnostico
FOR EACH ROW
BEGIN
    IF NEW.fecha > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha del diagnóstico no puede ser futura.';
    END IF;

    IF CHAR_LENGTH(TRIM(NEW.descripcion)) < 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La descripción del diagnóstico debe ser más detallada (mínimo 5 caracteres).';
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_diagnostico_valida_bu $$
CREATE TRIGGER trg_diagnostico_valida_bu
BEFORE UPDATE ON diagnostico
FOR EACH ROW
BEGIN
    IF NEW.fecha > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha del diagnóstico no puede ser futura.';
    END IF;

    IF CHAR_LENGTH(TRIM(NEW.descripcion)) < 5 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La descripción del diagnóstico debe ser más detallada (mínimo 5 caracteres).';
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.5 TRIGGERS DE PACIENTE
-- Evitan asignar pacientes a médicos no disponibles
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_paciente_medico_disponible_bi $$
CREATE TRIGGER trg_paciente_medico_disponible_bi
BEFORE INSERT ON paciente
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM vacaciones v
        WHERE v.id_empleado = NEW.id_empleado_medico
          AND CURDATE() BETWEEN v.fecha_inicio AND v.fecha_fin
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede asignar el paciente a un médico que está de vacaciones.';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM medico m
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        WHERE m.id_empleado = NEW.id_empleado_medico
          AND tm.nombre = 'Sustituto'
    )
    AND NOT EXISTS (
        SELECT 1
        FROM periodo_sustituto ps
        WHERE ps.id_empleado_medico = NEW.id_empleado_medico
          AND ps.fecha_ingreso <= CURDATE()
          AND (ps.fecha_retiro IS NULL OR CURDATE() <= ps.fecha_retiro)
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se puede asignar el paciente a un médico sustituto inactivo.';
    END IF;
END $$

DROP TRIGGER IF EXISTS trg_paciente_medico_disponible_bu $$
CREATE TRIGGER trg_paciente_medico_disponible_bu
BEFORE UPDATE ON paciente
FOR EACH ROW
BEGIN
    IF NEW.id_empleado_medico <> OLD.id_empleado_medico THEN
        IF EXISTS (
            SELECT 1
            FROM vacaciones v
            WHERE v.id_empleado = NEW.id_empleado_medico
              AND CURDATE() BETWEEN v.fecha_inicio AND v.fecha_fin
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No se puede reasignar el paciente a un médico que está de vacaciones.';
        END IF;

        IF EXISTS (
            SELECT 1
            FROM medico m
            JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
            WHERE m.id_empleado = NEW.id_empleado_medico
              AND tm.nombre = 'Sustituto'
        )
        AND NOT EXISTS (
            SELECT 1
            FROM periodo_sustituto ps
            WHERE ps.id_empleado_medico = NEW.id_empleado_medico
              AND ps.fecha_ingreso <= CURDATE()
              AND (ps.fecha_retiro IS NULL OR CURDATE() <= ps.fecha_retiro)
        ) THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No se puede reasignar el paciente a un médico sustituto inactivo.';
        END IF;
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.6 TRIGGER DE CONSISTENCIA EMPLEADO-MEDICO
-- Un empleado registrado como médico no debe tener
-- profesión no médica asignada
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_medico_empleado_profesion_bi $$
CREATE TRIGGER trg_medico_empleado_profesion_bi
BEFORE INSERT ON medico
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM empleado e
        WHERE e.id_empleado = NEW.id_empleado
          AND e.id_profesion IS NOT NULL
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Un médico no debe tener profesión de personal no médico asignada en empleado.';
    END IF;
END $$

DELIMITER ;

-- =====================================================
-- 3.7 TRIGGERS DE AUDITORIA
-- Registran operaciones importantes en la tabla auditoria
-- =====================================================

DELIMITER $$

DROP TRIGGER IF EXISTS trg_auditoria_paciente_ai $$
CREATE TRIGGER trg_auditoria_paciente_ai
AFTER INSERT ON paciente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria(tabla_afectada, operacion, descripcion)
    VALUES (
        'paciente',
        'INSERT',
        CONCAT('Se registró el paciente ID ', NEW.id_paciente,
               ' asignado al médico ID ', NEW.id_empleado_medico)
    );
END $$

DROP TRIGGER IF EXISTS trg_auditoria_diagnostico_ai $$
CREATE TRIGGER trg_auditoria_diagnostico_ai
AFTER INSERT ON diagnostico
FOR EACH ROW
BEGIN
    INSERT INTO auditoria(tabla_afectada, operacion, descripcion)
    VALUES (
        'diagnóstico',
        'INSERT',
        CONCAT('Se registró el diagnóstico ID ', NEW.id_diagnostico,
               ' para paciente ID ', NEW.id_paciente)
    );
END $$

DROP TRIGGER IF EXISTS trg_auditoria_vacaciones_ai $$
CREATE TRIGGER trg_auditoria_vacaciones_ai
AFTER INSERT ON vacaciones
FOR EACH ROW
BEGIN
    INSERT INTO auditoria(tabla_afectada, operacion, descripcion)
    VALUES (
        'vacaciones',
        'INSERT',
        CONCAT('Se registraron vacaciones ID ', NEW.id_vacacion,
               ' para empleado ID ', NEW.id_empleado)
    );
END $$

DELIMITER ;

-- =====================================================
-- 4. VISTA ADICIONAL: vw_sustitutos_estado
-- =====================================================

CREATE OR REPLACE VIEW vw_sustitutos_estado AS
SELECT
    m.id_empleado AS id_medico,
    e.nombre AS medico,
    ps.fecha_ingreso AS ultima_fecha_ingreso,
    ps.fecha_retiro AS fecha_retiro_ultimo_periodo,
    CASE
        WHEN ps.fecha_ingreso <= CURDATE()
         AND (ps.fecha_retiro IS NULL OR CURDATE() <= ps.fecha_retiro)
        THEN 'Activo'
        ELSE 'Inactivo'
    END AS estado_sustituto
FROM medico m
JOIN empleado e ON m.id_empleado = e.id_empleado
JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
LEFT JOIN periodo_sustituto ps
       ON ps.id_empleado_medico = m.id_empleado
      AND ps.fecha_ingreso = (
          SELECT MAX(ps2.fecha_ingreso)
          FROM periodo_sustituto ps2
          WHERE ps2.id_empleado_medico = m.id_empleado
      )
WHERE tm.nombre = 'Sustituto';

-- =====================================================
-- 5. PROCEDURES MEJORADOS (con validación de parámetros)
-- =====================================================

DELIMITER $$

DROP PROCEDURE IF EXISTS sp_pacientes_por_especialidad $$
CREATE PROCEDURE sp_pacientes_por_especialidad(IN p_especialidad VARCHAR(100))
BEGIN
    IF p_especialidad IS NULL OR TRIM(p_especialidad) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar una especialidad válida.';
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM especialidad WHERE nombre = p_especialidad
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La especialidad ingresada no existe en el sistema.';
    END IF;

    SELECT *
    FROM vw_pacientes_medicos
    WHERE especialidad = p_especialidad
    ORDER BY medico, paciente;
END $$

DROP PROCEDURE IF EXISTS sp_medicos_disponibles_por_especialidad $$
CREATE PROCEDURE sp_medicos_disponibles_por_especialidad(IN p_especialidad VARCHAR(100))
BEGIN
    IF p_especialidad IS NULL OR TRIM(p_especialidad) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar una especialidad válida.';
    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM especialidad
        WHERE nombre = p_especialidad
    ) THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La especialidad ingresada no existe en el sistema.';
    END IF;

    SELECT
        mi.id_medico,
        mi.medico,
        mi.num_licencia,
        mi.tipo_medico,
        mi.especialidad,
        COALESCE(
            GROUP_CONCAT(
                CONCAT(
                    h.dia_semana, ' ',
                    TIME_FORMAT(h.hora_inicio, '%H:%i'), '-',
                    TIME_FORMAT(h.hora_fin, '%H:%i')
                )
                ORDER BY FIELD(
                    h.dia_semana,
                    'Lunes','Martes','Miércoles','Jueves',
                    'Viernes','Sábado','Domingo'
                )
                SEPARATOR ' | '
            ),
            'Sin horario registrado'
        ) AS horarios
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
                AND ps.fecha_ingreso <= CURDATE()
                AND (
                    ps.fecha_retiro IS NULL
                    OR CURDATE() <= ps.fecha_retiro
                )
          )
      )
    GROUP BY mi.id_medico, mi.medico, mi.num_licencia,
             mi.tipo_medico, mi.especialidad
    ORDER BY mi.medico;
END $$

DROP PROCEDURE IF EXISTS sp_pacientes_por_diagnostico $$
CREATE PROCEDURE sp_pacientes_por_diagnostico(IN p_busqueda VARCHAR(100))
BEGIN
    IF p_busqueda IS NULL OR TRIM(p_busqueda) = '' THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar una enfermedad o palabra clave de diagnóstico.';
    END IF;

    SELECT *
    FROM vw_diagnosticos_pacientes
    WHERE diagnostico LIKE CONCAT('%', TRIM(p_busqueda), '%')
    ORDER BY fecha DESC, paciente;
END $$

DROP PROCEDURE IF EXISTS sp_vacaciones_medicos_intervalo $$
CREATE PROCEDURE sp_vacaciones_medicos_intervalo(
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    IF p_fecha_inicio IS NULL OR p_fecha_fin IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Debe ingresar fecha de inicio y fecha de fin.';
    END IF;

    IF p_fecha_fin < p_fecha_inicio THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha final no puede ser menor que la fecha inicial.';
    END IF;

    SELECT *
    FROM vw_vacaciones_medicos
    WHERE fecha_inicio <= p_fecha_fin
      AND fecha_fin >= p_fecha_inicio
    ORDER BY fecha_inicio, medico;
END $$

DELIMITER ;
