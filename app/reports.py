from db import fetch_dataframe


def pacientes_por_especialidad(especialidad: str):
    query = """
        SELECT
            id_paciente AS 'ID paciente',
            paciente AS 'Paciente',
            direccion_paciente AS 'Dirección',
            municipio_paciente AS 'Municipio',
            medico AS 'Médico responsable',
            num_licencia AS 'Licencia',
            especialidad AS 'Especialidad',
            tipo_medico AS 'Tipo médico'
        FROM vw_pacientes_medicos
        WHERE especialidad = %s
        ORDER BY medico, paciente;
    """
    return fetch_dataframe(query, (especialidad,))


def medicos_disponibles_por_especialidad(especialidad: str):
    query = """
        SELECT
            mi.id_medico AS 'ID médico',
            mi.medico AS 'Médico',
            mi.num_licencia AS 'Licencia',
            mi.tipo_medico AS 'Tipo médico',
            mi.especialidad AS 'Especialidad',
            mi.municipio AS 'Municipio',
            COALESCE(
                GROUP_CONCAT(
                    CONCAT(
                        h.dia_semana, ' ',
                        TIME_FORMAT(h.hora_inicio, '%H:%i'),
                        '-',
                        TIME_FORMAT(h.hora_fin, '%H:%i')
                    )
                    ORDER BY FIELD(h.dia_semana, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
                    SEPARATOR ' | '
                ),
                'Sin horario registrado'
            ) AS 'Horarios'
        FROM vw_medicos_info mi
        LEFT JOIN horario h
            ON mi.id_medico = h.id_empleado_medico
        WHERE mi.especialidad = %s
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
                    AND (
                        ps.fecha_retiro IS NULL
                        OR ps.fecha_ingreso > ps.fecha_retiro
                        OR CURDATE() <= ps.fecha_retiro
                    )
              )
          )
        GROUP BY
            mi.id_medico,
            mi.medico,
            mi.num_licencia,
            mi.tipo_medico,
            mi.especialidad,
            mi.municipio
        ORDER BY mi.medico;
    """
    return fetch_dataframe(query, (especialidad,))


def pacientes_por_diagnostico(texto_diagnostico: str):
    query = """
        SELECT
            id_diagnostico AS 'ID diagnóstico',
            fecha AS 'Fecha',
            diagnostico AS 'Diagnóstico',
            id_paciente AS 'ID paciente',
            paciente AS 'Paciente',
            direccion_paciente AS 'Dirección',
            municipio_paciente AS 'Municipio',
            medico AS 'Médico responsable',
            especialidad AS 'Especialidad'
        FROM vw_diagnosticos_pacientes
        WHERE diagnostico LIKE CONCAT('%', %s, '%')
        ORDER BY fecha DESC, paciente;
    """
    return fetch_dataframe(query, (texto_diagnostico,))


def vacaciones_medicos_intervalo(fecha_inicio, fecha_fin):
    query = """
        SELECT
            id_vacacion AS 'ID vacación',
            medico AS 'Médico',
            especialidad AS 'Especialidad',
            fecha_inicio AS 'Fecha inicio',
            fecha_fin AS 'Fecha fin',
            estado_vacaciones AS 'Estado'
        FROM vw_vacaciones_medicos
        WHERE fecha_inicio <= %s
          AND fecha_fin >= %s
        ORDER BY fecha_inicio, medico;
    """
    return fetch_dataframe(query, (fecha_fin, fecha_inicio))
