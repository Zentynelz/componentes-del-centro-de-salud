from db import fetch_dataframe


def resumen_dashboard():
    query = """
        SELECT
            (SELECT COUNT(*) FROM paciente) AS total_pacientes,
            (SELECT COUNT(*) FROM medico) AS total_medicos,
            (SELECT COUNT(*) FROM empleado) AS total_empleados,
            (SELECT COUNT(*) FROM diagnostico) AS total_diagnosticos,
            (SELECT COUNT(*) FROM horario) AS total_horarios,
            (SELECT COUNT(*) FROM vacaciones WHERE fecha_inicio > CURDATE()) AS vacaciones_planeadas;
    """
    return fetch_dataframe(query)


def agenda_hoy():
    query = """
        SELECT
            h.dia_semana AS 'Día',
            TIME_FORMAT(h.hora_inicio, '%H:%i') AS 'Inicio',
            TIME_FORMAT(h.hora_fin, '%H:%i') AS 'Fin',
            e.nombre AS 'Médico',
            esp.nombre AS 'Especialidad',
            tm.nombre AS 'Tipo'
        FROM horario h
        JOIN medico m ON h.id_empleado_medico = m.id_empleado
        JOIN empleado e ON m.id_empleado = e.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        WHERE h.dia_semana = ELT(WEEKDAY(CURDATE()) + 1, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo')
        ORDER BY h.hora_inicio, e.nombre;
    """
    return fetch_dataframe(query)


def agenda_por_dia(dia_semana: str):
    query = """
        SELECT
            h.id_horario AS 'ID',
            h.dia_semana AS 'Día',
            TIME_FORMAT(h.hora_inicio, '%H:%i') AS 'Inicio',
            TIME_FORMAT(h.hora_fin, '%H:%i') AS 'Fin',
            e.nombre AS 'Médico',
            esp.nombre AS 'Especialidad',
            tm.nombre AS 'Tipo médico'
        FROM horario h
        JOIN medico m ON h.id_empleado_medico = m.id_empleado
        JOIN empleado e ON m.id_empleado = e.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        WHERE h.dia_semana = %s
        ORDER BY h.hora_inicio, e.nombre;
    """
    return fetch_dataframe(query, (dia_semana,))


def agenda_semanal():
    query = """
        SELECT
            h.id_horario AS 'ID',
            h.dia_semana AS 'Día',
            TIME_FORMAT(h.hora_inicio, '%H:%i') AS 'Inicio',
            TIME_FORMAT(h.hora_fin, '%H:%i') AS 'Fin',
            e.nombre AS 'Médico',
            esp.nombre AS 'Especialidad',
            tm.nombre AS 'Tipo médico'
        FROM horario h
        JOIN medico m ON h.id_empleado_medico = m.id_empleado
        JOIN empleado e ON m.id_empleado = e.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        JOIN tipo_medico tm ON m.id_tipo = tm.id_tipo
        ORDER BY FIELD(h.dia_semana, 'Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo'), h.hora_inicio;
    """
    return fetch_dataframe(query)


def directorio_medicos(texto_busqueda: str = ""):
    query = """
        SELECT
            mi.id_medico AS 'ID',
            mi.medico AS 'Médico',
            mi.especialidad AS 'Especialidad',
            mi.tipo_medico AS 'Tipo',
            mi.num_licencia AS 'Licencia',
            mi.municipio AS 'Municipio',
            COALESCE(GROUP_CONCAT(te.telefono SEPARATOR ' / '), 'Sin teléfono') AS 'Teléfonos'
        FROM vw_medicos_info mi
        LEFT JOIN telefono_empleado te ON mi.id_medico = te.id_empleado
        WHERE mi.medico LIKE CONCAT('%', %s, '%')
           OR mi.especialidad LIKE CONCAT('%', %s, '%')
           OR mi.num_licencia LIKE CONCAT('%', %s, '%')
           OR mi.tipo_medico LIKE CONCAT('%', %s, '%')
        GROUP BY mi.id_medico, mi.medico, mi.especialidad, mi.tipo_medico, mi.num_licencia, mi.municipio
        ORDER BY mi.especialidad, mi.medico;
    """
    return fetch_dataframe(query, (texto_busqueda, texto_busqueda, texto_busqueda, texto_busqueda))


def buscar_pacientes(texto_busqueda: str = ""):
    query = """
        SELECT
            p.id_paciente AS 'ID',
            p.nombre AS 'Paciente',
            mu.nombre AS 'Municipio',
            p.direccion AS 'Dirección',
            em.nombre AS 'Médico responsable',
            esp.nombre AS 'Especialidad',
            COALESCE(GROUP_CONCAT(DISTINCT tp.telefono SEPARATOR ' / '), 'Sin teléfono') AS 'Teléfonos',
            COUNT(DISTINCT d.id_diagnostico) AS 'Diagnósticos'
        FROM paciente p
        JOIN municipio mu ON p.id_municipio = mu.id_municipio
        JOIN medico m ON p.id_empleado_medico = m.id_empleado
        JOIN empleado em ON m.id_empleado = em.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        LEFT JOIN telefono_paciente tp ON p.id_paciente = tp.id_paciente
        LEFT JOIN diagnostico d ON p.id_paciente = d.id_paciente
        WHERE p.nombre LIKE CONCAT('%', %s, '%')
           OR em.nombre LIKE CONCAT('%', %s, '%')
           OR esp.nombre LIKE CONCAT('%', %s, '%')
           OR mu.nombre LIKE CONCAT('%', %s, '%')
           OR CAST(p.id_paciente AS CHAR) = %s
        GROUP BY p.id_paciente, p.nombre, mu.nombre, p.direccion, em.nombre, esp.nombre
        ORDER BY p.nombre;
    """
    return fetch_dataframe(query, (texto_busqueda, texto_busqueda, texto_busqueda, texto_busqueda, texto_busqueda))


def ultimos_diagnosticos(limite: int = 10):
    limite = max(1, min(int(limite), 50))
    query = f"""
        SELECT
            d.id_diagnostico AS 'ID',
            d.fecha AS 'Fecha',
            p.nombre AS 'Paciente',
            d.descripcion AS 'Diagnóstico',
            em.nombre AS 'Médico responsable',
            esp.nombre AS 'Especialidad'
        FROM diagnostico d
        JOIN paciente p ON d.id_paciente = p.id_paciente
        JOIN medico m ON p.id_empleado_medico = m.id_empleado
        JOIN empleado em ON m.id_empleado = em.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        ORDER BY d.fecha DESC
        LIMIT {limite};
    """
    return fetch_dataframe(query)


def listado_vacaciones(texto_busqueda: str = ""):
    query = """
        SELECT
            v.id_vacacion AS 'ID',
            e.nombre AS 'Empleado',
            CASE WHEN m.id_empleado IS NULL THEN 'Empleado' ELSE 'Médico' END AS 'Clasificación',
            COALESCE(esp.nombre, 'No aplica') AS 'Especialidad',
            v.fecha_inicio AS 'Inicio',
            v.fecha_fin AS 'Fin',
            CASE
                WHEN CURDATE() > v.fecha_fin THEN 'Disfrutadas'
                WHEN CURDATE() BETWEEN v.fecha_inicio AND v.fecha_fin THEN 'En curso'
                ELSE 'Planeadas'
            END AS 'Estado'
        FROM vacaciones v
        JOIN empleado e ON v.id_empleado = e.id_empleado
        LEFT JOIN medico m ON e.id_empleado = m.id_empleado
        LEFT JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        WHERE e.nombre LIKE CONCAT('%', %s, '%')
           OR COALESCE(esp.nombre, '') LIKE CONCAT('%', %s, '%')
        ORDER BY v.fecha_inicio DESC;
    """
    return fetch_dataframe(query, (texto_busqueda, texto_busqueda))


def pacientes_por_especialidad(especialidad: str):
    query = """
        SELECT
            id_paciente AS 'ID paciente',
            paciente AS 'Paciente',
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
        LEFT JOIN horario h ON mi.id_medico = h.id_empleado_medico
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
                    AND (ps.fecha_retiro IS NULL OR CURDATE() <= ps.fecha_retiro)
              )
          )
        GROUP BY mi.id_medico, mi.medico, mi.num_licencia, mi.tipo_medico, mi.especialidad, mi.municipio
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
            id_vacacion AS 'ID',
            medico AS 'Médico',
            especialidad AS 'Especialidad',
            fecha_inicio AS 'Inicio',
            fecha_fin AS 'Fin',
            estado_vacaciones AS 'Estado'
        FROM vw_vacaciones_medicos
        WHERE fecha_inicio <= %s
          AND fecha_fin >= %s
        ORDER BY fecha_inicio, medico;
    """
    return fetch_dataframe(query, (fecha_fin, fecha_inicio))
