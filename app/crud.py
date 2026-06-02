# -*- coding: utf-8 -*-
"""
crud.py - Operaciones CRUD para VitalCare Centro de Salud
Incluye funciones para pacientes, diagnósticos, horarios,
vacaciones, usuarios, enfermedades e historial médico.
"""

from db import fetch_pairs, fetch_dataframe, execute_query

# ============================================================
# OPCIONES PARA DROPDOWNS
# ============================================================

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


def opciones_usuarios():
    """Retorna lista de usuarios activos para dropdown."""
    return fetch_pairs("""
        SELECT id_usuario, CONCAT(nombre_completo, ' (', rol, ')')
        FROM usuario
        WHERE activo = TRUE
        ORDER BY nombre_completo;
    """)


# ============================================================
# PACIENTES
# ============================================================

def obtener_paciente(id_paciente: int):
    df = fetch_dataframe("""
        SELECT id_paciente, id_municipio, id_empleado_medico, nombre, direccion
        FROM paciente
        WHERE id_paciente = %s;
    """, (id_paciente,))
    return None if df.empty else df.iloc[0]


def crear_paciente(nombre: str, direccion: str, id_municipio: int,
                   id_medico: int, id_usuario_creacion: int | None = None,
                   telefono: str | None = None):
    nuevo_id = execute_query("""
        INSERT INTO paciente (id_municipio, id_empleado_medico, id_usuario_creacion, nombre, direccion)
        VALUES (%s, %s, %s, %s, %s);
    """, (id_municipio, id_medico, id_usuario_creacion, nombre, direccion))

    if telefono and telefono.strip():
        execute_query("""
            INSERT INTO telefono_paciente (id_paciente, telefono)
            VALUES (%s, %s);
        """, (nuevo_id, telefono.strip()))

    return nuevo_id


def actualizar_paciente(id_paciente: int, nombre: str, direccion: str,
                        id_municipio: int, id_medico: int):
    execute_query("""
        UPDATE paciente
        SET nombre = %s, direccion = %s, id_municipio = %s, id_empleado_medico = %s
        WHERE id_paciente = %s;
    """, (nombre, direccion, id_municipio, id_medico, id_paciente))


def eliminar_paciente(id_paciente: int):
    execute_query("DELETE FROM paciente WHERE id_paciente = %s;", (id_paciente,))


# ============================================================
# DIAGNÓSTICOS
# ============================================================

def obtener_diagnostico(id_diagnostico: int):
    df = fetch_dataframe("""
        SELECT id_diagnostico, id_paciente, fecha, descripcion
        FROM diagnostico
        WHERE id_diagnostico = %s;
    """, (id_diagnostico,))
    return None if df.empty else df.iloc[0]


def crear_diagnostico(id_paciente: int, fecha, descripcion: str,
                      id_usuario_creacion: int | None = None,
                      id_enfermedad: int | None = None):
    return execute_query("""
        INSERT INTO diagnostico (id_paciente, id_usuario_creacion, id_enfermedad, fecha, descripcion)
        VALUES (%s, %s, %s, %s, %s);
    """, (id_paciente, id_usuario_creacion, id_enfermedad, fecha, descripcion))


def actualizar_diagnostico(id_diagnostico: int, fecha, descripcion: str):
    execute_query("""
        UPDATE diagnostico
        SET fecha = %s, descripcion = %s
        WHERE id_diagnostico = %s;
    """, (fecha, descripcion, id_diagnostico))


def eliminar_diagnostico(id_diagnostico: int):
    execute_query("DELETE FROM diagnostico WHERE id_diagnostico = %s;", (id_diagnostico,))


# ============================================================
# HORARIOS
# ============================================================

def crear_horario(id_medico: int, dia_semana: str, hora_inicio, hora_fin):
    return execute_query("""
        INSERT INTO horario (id_empleado_medico, dia_semana, hora_inicio, hora_fin)
        VALUES (%s, %s, %s, %s);
    """, (id_medico, dia_semana, hora_inicio, hora_fin))


def eliminar_horario(id_horario: int):
    execute_query("DELETE FROM horario WHERE id_horario = %s;", (id_horario,))


# ============================================================
# VACACIONES
# ============================================================

def crear_vacacion(id_empleado: int, fecha_inicio, fecha_fin):
    return execute_query("""
        INSERT INTO vacaciones (id_empleado, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s);
    """, (id_empleado, fecha_inicio, fecha_fin))


def eliminar_vacacion(id_vacacion: int):
    execute_query("DELETE FROM vacaciones WHERE id_vacacion = %s;", (id_vacacion,))


# ============================================================
# HISTORIAL MÉDICO (NUEVO)
# ============================================================

def historial_paciente(id_paciente: int):
    """Retorna DataFrame con todo el historial de diagnósticos de un paciente."""
    return fetch_dataframe("""
        SELECT d.fecha, d.descripcion,
               COALESCE(u.nombre_completo, '—') AS registrado_por,
               d.id_diagnostico
        FROM diagnostico d
        LEFT JOIN usuario u ON d.id_usuario_creacion = u.id_usuario
        WHERE d.id_paciente = %s
        ORDER BY d.fecha DESC, d.id_diagnostico DESC;
    """, (id_paciente,))


def pacientes_por_medico(id_medico: int):
    """Retorna los pacientes asignados a un médico específico."""
    return fetch_dataframe("""
        SELECT p.id_paciente, p.nombre AS paciente,
               m.id_medico, CONCAT(e.nombre, ' (', esp.nombre, ')') AS medico,
               p.direccion, mun.nombre AS municipio
        FROM paciente p
        JOIN vw_medicos_info m ON p.id_empleado_medico = m.id_medico
        JOIN empleado e ON m.id_medico = e.id_empleado
        JOIN especialidad esp ON m.id_especialidad = esp.id_especialidad
        JOIN municipio mun ON p.id_municipio = mun.id_municipio
        WHERE m.id_medico = %s
        ORDER BY p.nombre;
    """, (id_medico,))


def resumen_centro():
    """Retorna estadísticas generales del centro."""
    return fetch_dataframe("""
        SELECT
            (SELECT COUNT(*) FROM paciente) AS total_pacientes,
            (SELECT COUNT(*) FROM medico) AS total_medicos,
            (SELECT COUNT(*) FROM diagnostico) AS total_diagnosticos,
            (SELECT COUNT(*) FROM usuario WHERE activo = TRUE) AS total_usuarios,
            (SELECT COUNT(*) FROM horario) AS total_horarios,
            (SELECT COUNT(*) FROM enfermedad) AS total_enfermedades;
    """)


# ============================================================
# USUARIOS (para administración)
# ============================================================

def listar_usuarios_completo():
    """Retorna todos los usuarios para gestión administrativa."""
    return fetch_dataframe("""
        SELECT id_usuario, username, nombre_completo, rol, activo, fecha_creacion
        FROM usuario
        ORDER BY activo DESC, nombre_completo;
    """)


def obtener_usuario(id_usuario: int):
    """Retorna un usuario por ID."""
    df = fetch_dataframe("""
        SELECT id_usuario, username, nombre_completo, rol, activo
        FROM usuario WHERE id_usuario = %s;
    """, (id_usuario,))
    return None if df.empty else df.iloc[0]


def crear_usuario(username: str, password_hash: str, nombre_completo: str, rol: str) -> int:
    """Crea un nuevo usuario."""
    return execute_query("""
        INSERT INTO usuario (username, password_hash, nombre_completo, rol)
        VALUES (%s, %s, %s, %s);
    """, (username, password_hash, nombre_completo, rol))


def actualizar_usuario(id_usuario: int, nombre_completo: str, rol: str, activo: bool):
    """Actualiza datos de un usuario."""
    execute_query("""
        UPDATE usuario SET nombre_completo = %s, rol = %s, activo = %s
        WHERE id_usuario = %s;
    """, (nombre_completo, rol, activo, id_usuario))


def actualizar_password(id_usuario: int, password_hash: str):
    """Cambia la contraseña de un usuario."""
    execute_query("""
        UPDATE usuario SET password_hash = %s WHERE id_usuario = %s;
    """, (password_hash, id_usuario))


# ============================================================
# CRUD DE MÉDICOS
# ============================================================

def crear_medico(nombre: str, direccion: str, id_municipio: int,
                 id_profesion: int, num_licencia: str,
                 id_especialidad: int, id_tipo: int) -> int:
    """
    Crea un empleado + médico (dos INSERTS en transacción).
    Retorna el id_empleado (= id_medico).
    """
    # 1. Insertar empleado
    id_emp = execute_query("""
        INSERT INTO empleado (id_municipio, id_profesion, nombre, direccion)
        VALUES (%s, %s, %s, %s);
    """, (id_municipio, id_profesion, nombre, direccion))

    # 2. Insertar médico
    execute_query("""
        INSERT INTO medico (id_empleado, num_licencia, id_tipo, id_especialidad)
        VALUES (%s, %s, %s, %s);
    """, (id_emp, num_licencia, id_tipo, id_especialidad))

    return id_emp


def eliminar_medico(id_medico: int):
    """
    Elimina un médico (CASCADE borra el empleado asociado).
    """
    execute_query("DELETE FROM medico WHERE id_empleado = %s;", (id_medico,))


def obtener_medico(id_medico: int):
    """Retorna datos completos de un médico para edición."""
    return fetch_dataframe("""
        SELECT e.id_empleado AS id_medico, e.nombre, e.direccion,
               e.id_municipio, e.id_profesion,
               m.num_licencia, m.id_especialidad, m.id_tipo
        FROM empleado e
        JOIN medico m ON e.id_empleado = m.id_empleado
        WHERE e.id_empleado = %s;
    """, (id_medico,))


def actualizar_medico(id_medico: int, nombre: str, direccion: str,
                      id_municipio: int, id_profesion: int,
                      num_licencia: str, id_especialidad: int, id_tipo: int):
    """Actualiza datos de empleado + médico."""
    execute_query("""
        UPDATE empleado SET nombre = %s, direccion = %s,
            id_municipio = %s, id_profesion = %s
        WHERE id_empleado = %s;
    """, (nombre, direccion, id_municipio, id_profesion, id_medico))
    execute_query("""
        UPDATE medico SET num_licencia = %s, id_especialidad = %s, id_tipo = %s
        WHERE id_empleado = %s;
    """, (num_licencia, id_especialidad, id_tipo, id_medico))


def opciones_profesiones():
    return fetch_pairs("SELECT id_profesion, nombre FROM profesion ORDER BY nombre;")


def opciones_especialidades():
    return fetch_pairs("SELECT id_especialidad, nombre FROM especialidad ORDER BY nombre;")


def opciones_tipos_medico():
    return fetch_pairs("SELECT id_tipo, nombre FROM tipo_medico ORDER BY nombre;")
