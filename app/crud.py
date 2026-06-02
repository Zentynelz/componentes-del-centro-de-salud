from db import fetch_pairs, fetch_dataframe, execute_query


def opciones_municipios():
    return fetch_pairs("SELECT id_municipio, nombre FROM municipio ORDER BY nombre;")


def opciones_medicos():
    return fetch_pairs("""
        SELECT id_medico, CONCAT(medico, ' — ', especialidad, ' — ', tipo_medico)
        FROM vw_medicos_info
        ORDER BY medico;
    """)


def opciones_empleados():
    return fetch_pairs("""
        SELECT id_empleado, nombre
        FROM empleado
        ORDER BY nombre;
    """)


def opciones_pacientes():
    return fetch_pairs("""
        SELECT p.id_paciente, CONCAT(p.nombre, ' — Médico: ', e.nombre)
        FROM paciente p
        JOIN medico m ON p.id_empleado_medico = m.id_empleado
        JOIN empleado e ON m.id_empleado = e.id_empleado
        ORDER BY p.nombre;
    """)


def opciones_diagnosticos():
    return fetch_pairs("""
        SELECT d.id_diagnostico, CONCAT(d.id_diagnostico, ' — ', p.nombre, ' — ', d.descripcion)
        FROM diagnostico d
        JOIN paciente p ON d.id_paciente = p.id_paciente
        ORDER BY d.fecha DESC, d.id_diagnostico DESC;
    """)


def opciones_horarios():
    return fetch_pairs("""
        SELECT h.id_horario,
               CONCAT(h.id_horario, ' — ', e.nombre, ' — ', h.dia_semana, ' ',
                      TIME_FORMAT(h.hora_inicio, '%H:%i'), '-', TIME_FORMAT(h.hora_fin, '%H:%i'))
        FROM horario h
        JOIN medico m ON h.id_empleado_medico = m.id_empleado
        JOIN empleado e ON m.id_empleado = e.id_empleado
        ORDER BY h.id_horario DESC;
    """)


def opciones_enfermedades():
    return fetch_pairs("""
        SELECT id_enfermedad, nombre
        FROM enfermedad
        ORDER BY nombre;
    """)


def opciones_vacaciones():
    return fetch_pairs("""
        SELECT v.id_vacacion,
               CONCAT(v.id_vacacion, ' — ', e.nombre, ' — ', v.fecha_inicio, ' a ', v.fecha_fin)
        FROM vacaciones v
        JOIN empleado e ON v.id_empleado = e.id_empleado
        ORDER BY v.fecha_inicio DESC;
    """)


def obtener_paciente(id_paciente: int):
    df = fetch_dataframe("""
        SELECT id_paciente, id_municipio, id_empleado_medico, nombre, direccion
        FROM paciente
        WHERE id_paciente = %s;
    """, (id_paciente,))
    return None if df.empty else df.iloc[0]


def obtener_diagnostico(id_diagnostico: int):
    df = fetch_dataframe("""
        SELECT id_diagnostico, id_paciente, fecha, descripcion
        FROM diagnostico
        WHERE id_diagnostico = %s;
    """, (id_diagnostico,))
    return None if df.empty else df.iloc[0]


def crear_paciente(nombre: str, direccion: str, id_municipio: int, id_medico: int, telefono: str | None = None):
    nuevo_id = execute_query("""
        INSERT INTO paciente (id_municipio, id_empleado_medico, nombre, direccion)
        VALUES (%s, %s, %s, %s);
    """, (id_municipio, id_medico, nombre, direccion))

    if telefono and telefono.strip():
        execute_query("""
            INSERT INTO telefono_paciente (id_paciente, telefono)
            VALUES (%s, %s);
        """, (nuevo_id, telefono.strip()))

    return nuevo_id


def actualizar_paciente(id_paciente: int, nombre: str, direccion: str, id_municipio: int, id_medico: int):
    execute_query("""
        UPDATE paciente
        SET nombre = %s,
            direccion = %s,
            id_municipio = %s,
            id_empleado_medico = %s
        WHERE id_paciente = %s;
    """, (nombre, direccion, id_municipio, id_medico, id_paciente))


def eliminar_paciente(id_paciente: int):
    execute_query("DELETE FROM paciente WHERE id_paciente = %s;", (id_paciente,))


def crear_diagnostico(id_paciente: int, fecha, descripcion: str):
    return execute_query("""
        INSERT INTO diagnostico (id_paciente, fecha, descripcion)
        VALUES (%s, %s, %s);
    """, (id_paciente, fecha, descripcion))


def actualizar_diagnostico(id_diagnostico: int, fecha, descripcion: str):
    execute_query("""
        UPDATE diagnostico
        SET fecha = %s,
            descripcion = %s
        WHERE id_diagnostico = %s;
    """, (fecha, descripcion, id_diagnostico))


def eliminar_diagnostico(id_diagnostico: int):
    execute_query("DELETE FROM diagnostico WHERE id_diagnostico = %s;", (id_diagnostico,))


def crear_horario(id_medico: int, dia_semana: str, hora_inicio, hora_fin):
    return execute_query("""
        INSERT INTO horario (id_empleado_medico, dia_semana, hora_inicio, hora_fin)
        VALUES (%s, %s, %s, %s);
    """, (id_medico, dia_semana, hora_inicio, hora_fin))


def eliminar_horario(id_horario: int):
    execute_query("DELETE FROM horario WHERE id_horario = %s;", (id_horario,))


def crear_vacacion(id_empleado: int, fecha_inicio, fecha_fin):
    return execute_query("""
        INSERT INTO vacaciones (id_empleado, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s);
    """, (id_empleado, fecha_inicio, fecha_fin))


def eliminar_vacacion(id_vacacion: int):
    execute_query("DELETE FROM vacaciones WHERE id_vacacion = %s;", (id_vacacion,))
