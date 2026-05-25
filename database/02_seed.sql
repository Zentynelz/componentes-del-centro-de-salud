USE centro_salud;

INSERT INTO municipio (nombre) VALUES
('Bogotá'),
('Soacha'),
('Chía'),
('Facatativá'),
('Zipaquirá');

INSERT INTO profesion (nombre) VALUES
('Auxiliar de enfermería'),
('Vigilante'),
('Administrativo');

INSERT INTO especialidad (nombre) VALUES
('Medicina General'),
('Pediatría'),
('Cardiología'),
('Dermatología'),
('Ginecología');

INSERT INTO tipo_medico (nombre) VALUES
('Titular'),
('Interino'),
('Sustituto');

INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion) VALUES
(1, NULL, 'Ana María Torres', 'Cra 10 # 20-30'),
(1, NULL, 'Carlos Pérez Gómez', 'Calle 45 # 12-80'),
(2, NULL, 'Laura Rodríguez Díaz', 'Av Siempre Viva # 123'),
(3, NULL, 'Miguel Ángel Rojas', 'Cra 7 # 90-15'),
(4, NULL, 'Sofía Martínez León', 'Calle 8 # 5-22'),
(1, 1, 'Diana Carolina Ruiz', 'Calle 30 # 15-40'),
(2, 2, 'Jorge Eliécer Ramos', 'Cra 9 # 13-17'),
(1, 3, 'Patricia Moreno Silva', 'Av Caracas # 40-55');

INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad) VALUES
(1, 'LIC-MG-001', 1, 1),
(2, 'LIC-PED-002', 2, 2),
(3, 'LIC-CAR-003', 1, 3),
(4, 'LIC-DER-004', 3, 4),
(5, 'LIC-GIN-005', 3, 5);

INSERT INTO telefono_empleado (id_empleado, telefono) VALUES
(1, '3001112233'),
(1, '6012223344'),
(2, '3002223344'),
(3, '3003334455'),
(4, '3004445566'),
(5, '3005556677'),
(6, '3006667788'),
(7, '3007778899'),
(8, '3008889900');

INSERT INTO horario (id_empleado_medico, dia_semana, hora_inicio, hora_fin) VALUES
(1, 'Lunes', '08:00:00', '12:00:00'),
(1, 'Miércoles', '08:00:00', '12:00:00'),
(2, 'Martes', '09:00:00', '13:00:00'),
(2, 'Jueves', '09:00:00', '13:00:00'),
(3, 'Lunes', '14:00:00', '18:00:00'),
(3, 'Viernes', '08:00:00', '12:00:00'),
(4, 'Miércoles', '13:00:00', '17:00:00'),
(5, 'Jueves', '07:00:00', '11:00:00');

INSERT INTO periodo_sustituto (id_empleado_medico, fecha_ingreso, fecha_retiro) VALUES
(4, '2024-02-01', '2024-05-31'),
(4, '2025-01-15', NULL),
(5, '2025-03-01', NULL);

INSERT INTO vacaciones (id_empleado, fecha_inicio, fecha_fin) VALUES
(1, '2024-12-15', '2024-12-30'),
(2, '2025-06-10', '2025-06-20'),
(3, '2025-01-05', '2025-01-12'),
(4, '2025-08-01', '2025-08-15'),
(6, '2025-07-01', '2025-07-10');

INSERT INTO paciente (id_municipio, id_empleado_medico, nombre, direccion) VALUES
(1, 1, 'Juan Sebastián López', 'Calle 11 # 22-33'),
(2, 1, 'María Fernanda Castro', 'Cra 20 # 10-40'),
(1, 2, 'Camila Andrea Vargas', 'Av Boyacá # 55-10'),
(3, 2, 'Santiago Herrera', 'Calle 70 # 8-21'),
(4, 3, 'Andrés Felipe Muñoz', 'Cra 5 # 14-99'),
(5, 3, 'Natalia Gómez Prieto', 'Calle 6 # 3-50'),
(1, 4, 'Valentina Rincón', 'Av Suba # 100-20'),
(2, 5, 'Paula Alejandra Méndez', 'Calle 1 # 2-3');

INSERT INTO telefono_paciente (id_paciente, telefono) VALUES
(1, '3101002001'),
(1, '6013004001'),
(2, '3101002002'),
(3, '3101002003'),
(4, '3101002004'),
(5, '3101002005'),
(6, '3101002006'),
(7, '3101002007'),
(8, '3101002008');

INSERT INTO diagnostico (id_paciente, fecha, descripcion) VALUES
(1, '2025-01-10', 'Hipertensión arterial leve'),
(1, '2025-02-14', 'Control general sin complicaciones'),
(2, '2025-03-05', 'Diabetes tipo 2'),
(3, '2025-03-20', 'Bronquitis aguda'),
(4, '2025-04-15', 'Asma infantil'),
(5, '2025-04-22', 'Hipertensión arterial'),
(6, '2025-05-03', 'Arritmia cardiaca'),
(7, '2025-05-12', 'Dermatitis alérgica'),
(8, '2025-05-19', 'Control prenatal');
