USE centro_salud;

CALL sp_pacientes_por_especialidad('Cardiología');
CALL sp_medicos_disponibles_por_especialidad('Cardiología');
CALL sp_pacientes_por_diagnostico('Hipertensión');
CALL sp_vacaciones_medicos_intervalo('2025-01-01', '2025-12-31');

SELECT * FROM vw_pacientes_medicos;
SELECT * FROM vw_medicos_info;
SELECT * FROM vw_diagnosticos_pacientes;
SELECT * FROM vw_vacaciones_medicos;
