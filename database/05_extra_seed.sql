USE centro_salud;

-- =========================================================
-- DATOS ADICIONALES PARA DEMOSTRACIÓN DEL PORTAL
-- Ejecutar una sola vez después de:
-- 01_schema.sql, 02_seed.sql y 03_views_procedures_triggers.sql
-- =========================================================

INSERT INTO municipio (nombre) VALUES
('Cajicá'),
('Madrid'),
('Mosquera'),
('Funza'),
('La Calera')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

INSERT INTO especialidad (nombre) VALUES
('Ortopedia'),
('Neurología'),
('Oftalmología'),
('Psicología'),
('Urología')
ON DUPLICATE KEY UPDATE nombre = VALUES(nombre);

-- Guardar IDs de municipios
SELECT id_municipio INTO @mun_bogota FROM municipio WHERE nombre = 'Bogotá' LIMIT 1;
SELECT id_municipio INTO @mun_soacha FROM municipio WHERE nombre = 'Soacha' LIMIT 1;
SELECT id_municipio INTO @mun_chia FROM municipio WHERE nombre = 'Chía' LIMIT 1;
SELECT id_municipio INTO @mun_cajica FROM municipio WHERE nombre = 'Cajicá' LIMIT 1;
SELECT id_municipio INTO @mun_madrid FROM municipio WHERE nombre = 'Madrid' LIMIT 1;
SELECT id_municipio INTO @mun_mosquera FROM municipio WHERE nombre = 'Mosquera' LIMIT 1;
SELECT id_municipio INTO @mun_funza FROM municipio WHERE nombre = 'Funza' LIMIT 1;
SELECT id_municipio INTO @mun_calera FROM municipio WHERE nombre = 'La Calera' LIMIT 1;

-- Guardar IDs de especialidades y tipos
SELECT id_especialidad INTO @esp_mg FROM especialidad WHERE nombre = 'Medicina General' LIMIT 1;
SELECT id_especialidad INTO @esp_ped FROM especialidad WHERE nombre = 'Pediatría' LIMIT 1;
SELECT id_especialidad INTO @esp_car FROM especialidad WHERE nombre = 'Cardiología' LIMIT 1;
SELECT id_especialidad INTO @esp_der FROM especialidad WHERE nombre = 'Dermatología' LIMIT 1;
SELECT id_especialidad INTO @esp_gin FROM especialidad WHERE nombre = 'Ginecología' LIMIT 1;
SELECT id_especialidad INTO @esp_ort FROM especialidad WHERE nombre = 'Ortopedia' LIMIT 1;
SELECT id_especialidad INTO @esp_neu FROM especialidad WHERE nombre = 'Neurología' LIMIT 1;
SELECT id_especialidad INTO @esp_oft FROM especialidad WHERE nombre = 'Oftalmología' LIMIT 1;
SELECT id_especialidad INTO @esp_psi FROM especialidad WHERE nombre = 'Psicología' LIMIT 1;
SELECT id_especialidad INTO @esp_uro FROM especialidad WHERE nombre = 'Urología' LIMIT 1;

SELECT id_tipo INTO @tipo_titular FROM tipo_medico WHERE nombre = 'Titular' LIMIT 1;
SELECT id_tipo INTO @tipo_interino FROM tipo_medico WHERE nombre = 'Interino' LIMIT 1;
SELECT id_tipo INTO @tipo_sustituto FROM tipo_medico WHERE nombre = 'Sustituto' LIMIT 1;

-- Nuevos médicos
INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
VALUES (@mun_bogota, NULL, 'Felipe Cárdenas Mora', 'Av. Esperanza # 45-90');
SET @med_ort = LAST_INSERT_ID();
INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
VALUES (@med_ort, 'LIC-ORT-006', @tipo_titular, @esp_ort);

INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
VALUES (@mun_chia, NULL, 'Juliana Acosta Bernal', 'Cra 12 # 18-44');
SET @med_neu = LAST_INSERT_ID();
INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
VALUES (@med_neu, 'LIC-NEU-007', @tipo_interino, @esp_neu);

INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
VALUES (@mun_mosquera, NULL, 'Ricardo Ávila Pardo', 'Calle 9 # 23-11');
SET @med_oft = LAST_INSERT_ID();
INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
VALUES (@med_oft, 'LIC-OFT-008', @tipo_titular, @esp_oft);

INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
VALUES (@mun_funza, NULL, 'Manuela Prieto Salas', 'Cra 3 # 6-72');
SET @med_psi = LAST_INSERT_ID();
INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
VALUES (@med_psi, 'LIC-PSI-009', @tipo_sustituto, @esp_psi);

INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
VALUES (@mun_calera, NULL, 'Óscar Villamizar Reyes', 'Vereda El Hato Casa 14');
SET @med_uro = LAST_INSERT_ID();
INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
VALUES (@med_uro, 'LIC-URO-010', @tipo_interino, @esp_uro);

-- Teléfonos de médicos nuevos
INSERT INTO telefono_empleado (id_empleado, telefono) VALUES
(@med_ort, '3019001001'),
(@med_neu, '3019001002'),
(@med_oft, '3019001003'),
(@med_psi, '3019001004'),
(@med_uro, '3019001005');

-- Horarios adicionales
INSERT INTO horario (id_empleado_medico, dia_semana, hora_inicio, hora_fin) VALUES
(@med_ort, 'Lunes', '07:00:00', '11:00:00'),
(@med_ort, 'Jueves', '14:00:00', '18:00:00'),
(@med_neu, 'Martes', '08:00:00', '12:00:00'),
(@med_neu, 'Viernes', '13:00:00', '17:00:00'),
(@med_oft, 'Miércoles', '08:00:00', '12:00:00'),
(@med_oft, 'Sábado', '08:00:00', '11:00:00'),
(@med_psi, 'Lunes', '13:00:00', '17:00:00'),
(@med_psi, 'Miércoles', '13:00:00', '17:00:00'),
(@med_uro, 'Jueves', '08:00:00', '12:00:00'),
(@med_uro, 'Viernes', '08:00:00', '12:00:00');

-- Sustitución activa para psicología
INSERT INTO periodo_sustituto (id_empleado_medico, fecha_ingreso, fecha_retiro) VALUES
(@med_psi, '2025-02-10', NULL);

-- Pacientes adicionales
INSERT INTO paciente (id_municipio, id_empleado_medico, nombre, direccion) VALUES
(@mun_bogota, @med_ort, 'Brayan Estiven Molina', 'Calle 80 # 90-10'),
(@mun_madrid, @med_ort, 'Lorena Paola Suárez', 'Cra 4 # 15-30'),
(@mun_chia, @med_neu, 'Tomás Andrés Castaño', 'Av Pradilla # 2-22'),
(@mun_cajica, @med_neu, 'Isabella Cortés Medina', 'Calle 5 # 7-80'),
(@mun_mosquera, @med_oft, 'Mateo Salazar Niño', 'Cra 12 # 10-10'),
(@mun_funza, @med_oft, 'Gabriela Pineda Ruiz', 'Calle 14 # 3-33'),
(@mun_bogota, @med_psi, 'Daniela Ramírez Vega', 'Av 68 # 45-20'),
(@mun_soacha, @med_psi, 'Esteban Felipe Arias', 'Calle 22 # 1-19'),
(@mun_calera, @med_uro, 'Fernando Gómez Abril', 'Km 4 vía La Calera'),
(@mun_bogota, @med_uro, 'Mónica Patricia León', 'Cra 30 # 60-45'),
(@mun_chia, 1, 'Julián David Torres', 'Calle 1 # 1-21'),
(@mun_soacha, 2, 'Sara Valentina Méndez', 'Cra 8 # 19-40'),
(@mun_bogota, 3, 'Héctor Alfonso Peña', 'Av Suba # 120-09'),
(@mun_funza, 4, 'Luisa Fernanda Ortiz', 'Calle 7 # 5-05'),
(@mun_madrid, 5, 'Carolina Bustamante Ríos', 'Cra 6 # 8-42');

-- Teléfonos para pacientes adicionales
INSERT INTO telefono_paciente (id_paciente, telefono)
SELECT id_paciente, CONCAT('31255', LPAD(id_paciente, 5, '0'))
FROM paciente
WHERE id_paciente > 8;

-- Diagnósticos adicionales
INSERT INTO diagnostico (id_paciente, fecha, descripcion) VALUES
(9, '2025-06-02', 'Esguince de tobillo grado I'),
(10, '2025-06-03', 'Dolor lumbar mecánico'),
(11, '2025-06-04', 'Migraña crónica'),
(12, '2025-06-05', 'Cefalea tensional'),
(13, '2025-06-06', 'Miopía y fatiga visual'),
(14, '2025-06-07', 'Conjuntivitis alérgica'),
(15, '2025-06-08', 'Ansiedad generalizada'),
(16, '2025-06-09', 'Trastorno del sueño'),
(17, '2025-06-10', 'Infección urinaria'),
(18, '2025-06-11', 'Cálculo renal en observación'),
(19, '2025-06-12', 'Control general preventivo'),
(20, '2025-06-13', 'Rinitis alérgica'),
(21, '2025-06-14', 'Hipertensión arterial controlada'),
(22, '2025-06-15', 'Dermatitis de contacto'),
(23, '2025-06-16', 'Control ginecológico');

-- Vacaciones adicionales
INSERT INTO vacaciones (id_empleado, fecha_inicio, fecha_fin) VALUES
(@med_ort, '2025-09-01', '2025-09-10'),
(@med_neu, '2025-10-05', '2025-10-15'),
(@med_oft, '2025-11-20', '2025-11-30'),
(@med_psi, '2025-12-01', '2025-12-07'),
(@med_uro, '2025-08-18', '2025-08-25');
