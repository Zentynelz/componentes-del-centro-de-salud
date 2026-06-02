-- =====================================================
-- ARCHIVO: 08_usuarios_y_login.sql
-- DESCRIPCION: Sistema de usuarios, login y roles
-- ORDEN: Ejecutar DESPUES de 07_enfermedades_y_extra.sql
-- =====================================================

USE centro_salud;

-- =====================================================
-- 1. TABLA: usuario
-- =====================================================
CREATE TABLE IF NOT EXISTS usuario (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    nombre_completo VARCHAR(120) NOT NULL,
    rol ENUM('admin', 'medico', 'enfermero', 'recepcionista') NOT NULL DEFAULT 'medico',
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Usuario admin por defecto (password: admin123)
INSERT INTO usuario (username, password_hash, nombre_completo, rol)
VALUES ('admin', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Administrador', 'admin')
ON DUPLICATE KEY UPDATE username = username;

-- Algunos usuarios de prueba
INSERT INTO usuario (username, password_hash, nombre_completo, rol) VALUES
('dr.garcia', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Dr. Carlos García', 'medico'),
('enfermera.lopez', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Enf. María López', 'enfermero'),
('recepcion', '240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9', 'Recepcionista', 'recepcionista')
ON DUPLICATE KEY UPDATE username = VALUES(username);

-- =====================================================
-- 2. MODIFICAR TABLAS EXISTENTES
-- =====================================================

-- Agregar id_usuario_creacion a paciente
ALTER TABLE paciente
ADD COLUMN id_usuario_creacion INT DEFAULT NULL AFTER id_empleado_medico,
ADD CONSTRAINT fk_paciente_usuario
    FOREIGN KEY (id_usuario_creacion) REFERENCES usuario(id_usuario)
    ON DELETE SET NULL;

-- Agregar id_usuario_creacion a diagnostico
ALTER TABLE diagnostico
ADD COLUMN id_usuario_creacion INT DEFAULT NULL AFTER id_paciente,
ADD CONSTRAINT fk_diagnostico_usuario
    FOREIGN KEY (id_usuario_creacion) REFERENCES usuario(id_usuario)
    ON DELETE SET NULL;

-- =====================================================
-- 3. VISTA: vw_usuarios_activos (para login)
-- =====================================================
CREATE OR REPLACE VIEW vw_usuarios_activos AS
SELECT id_usuario, username, password_hash, nombre_completo, rol
FROM usuario
WHERE activo = TRUE;

-- =====================================================
-- 4. ACTUALIZAR TRIGGER de auditoría para incluir usuario
-- =====================================================
-- Nota: Los triggers existentes se mantienen, pero la app
-- ahora registrará quién hizo cada operación vía las tablas
