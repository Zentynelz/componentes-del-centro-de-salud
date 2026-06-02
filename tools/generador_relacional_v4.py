"""
Generador del Diagrama Relacional - Versión 5 (actualizado junio 2026)
======================================================================
- Nombre de tabla FUERA de la caja (arriba)
- Separación visual: sección de llaves (PK + FK) | sección de atributos no-llave
- PK amarillo subrayado, FK azul claro (SIN etiquetas PK/FK en el nombre)
- Columnas que son PK y FK a la vez: color amarillo subrayado (PK prevalece)
- Sin texto en flechas, fondo oscuro
- 16 tablas: se agregaron USUARIO, ENFERMEDAD, AUDITORIA
- PACIENTE y DIAGNOSTICO ahora tienen FK id_usuario_creacion → USUARIO
"""

import urllib.request
import os

def make_label(name, bg, pk_only, pk_fk, fk_only, normal):
    """
    Genera el HTML-like label para Graphviz.
    
    Orden dentro de la caja:
      1. PK-only: amarillo subrayado, etiqueta (PK)
      2. PK+FK:   amarillo subrayado, etiqueta (PK, FK)
      3. FK-only: azul claro, etiqueta (FK)
      4. ── divisor visual ── (solo si hay columnas no-llave)
      5. No-llave: blanco
    """
    rows = []

    # ── Outer TABLE (BORDER=0) required by Graphviz HTML label spec ──
    rows.append('<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0">')

    # ── Nombre de tabla FUERA de la caja ──
    rows.append(f'<TR><TD BORDER="0" WIDTH="220" ALIGN="CENTER"><FONT COLOR="white"><B>{name}</B></FONT></TD></TR>')

    # ── Caja con borde ──
    rows.append('<TR><TD BORDER="0" CELLPADDING="0">')
    rows.append(f'<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="5" BGCOLOR="{bg}">')

    has_separator = len(normal) > 0

    # 1. PK-only (color amarillo subrayado, sin etiqueta PK)
    for col in pk_only:
        rows.append(f'<TR><TD ALIGN="LEFT" BORDER="0"><FONT COLOR="#e8d44d"><U>{col}</U></FONT></TD></TR>')

    # 2. PK + FK (color amarillo subrayado, sin etiqueta)
    for col in pk_fk:
        rows.append(f'<TR><TD ALIGN="LEFT" BORDER="0"><FONT COLOR="#e8d44d"><U>{col}</U></FONT></TD></TR>')

    # 3. FK-only (color azul claro, sin etiqueta FK)
    for col in fk_only:
        rows.append(f'<TR><TD ALIGN="LEFT" BORDER="0"><FONT COLOR="#7eb8da">{col}</FONT></TD></TR>')

    # 4. Divisor
    if has_separator:
        rows.append(f'<TR><TD BORDER="0" BGCOLOR="#3a5a7a" HEIGHT="2"></TD></TR>')

    # 5. No-llave
    for col in normal:
        rows.append(f'<TR><TD ALIGN="LEFT" BORDER="0"><FONT COLOR="white">{col}</FONT></TD></TR>')

    rows.append('</TABLE>')
    rows.append('</TD></TR>')

    # ── Cierre del outer TABLE ──
    rows.append('</TABLE>')

    return '\n'.join(rows)


# ──────────────────────────────────────────────────────────────────────
# DEFINICIÓN DE TABLAS
# ──────────────────────────────────────────────────────────────────────
# Cada tupla: (node_id, display_name, bg_color, pk_only, pk_fk, fk_only, normal)

param = [  # fila superior — paramétricas
    ("MUNICIPIO",         "MUNICIPIO",      "#16213e", ["id_municipio"], [], [], ["nombre"]),
    ("PROFESION",         "PROFESION",      "#16213e", ["id_profesion"], [], [], ["nombre"]),
    ("ESPECIALIDAD",      "ESPECIALIDAD",   "#16213e", ["id_especialidad"], [], [], ["nombre"]),
    ("TIPO_MEDICO",       "TIPO M\u00c9DICO", "#16213e", ["id_tipo"], [], [], ["nombre"]),
    ("ENFERMEDAD",        "ENFERMEDAD",     "#16213e", ["id_enfermedad"], [], [], ["nombre"]),
]

main = [  # fila media — principales
    ("EMPLEADO",          "EMPLEADO",       "#0f3460",
        ["id_empleado"], [],
        ["id_municipio", "id_profesion"],
        ["nombre", "direccion"]),

    ("MEDICO",            "M\u00c9DICO",      "#0f3460",
        [],
        ["id_empleado"],
        ["id_tipo", "id_especialidad"],
        ["num_licencia"]),
]

dep = [  # fila inferior — dependientes
    ("PACIENTE",          "PACIENTE",       "#0f3460",
        ["id_paciente"], [],
        ["id_municipio", "id_empleado_medico", "id_usuario_creacion"],
        ["nombre", "direccion"]),

    ("HORARIO",           "HORARIO",        "#0f3460",
        ["id_horario"], [],
        ["id_empleado_medico"],
        ["dia_semana", "hora_inicio", "hora_fin"]),

    ("PERIODO_SUSTITUTO", "PERIODO SUSTITUTO", "#0f3460",
        ["id_periodo"], [],
        ["id_empleado_medico"],
        ["fecha_ingreso", "fecha_retiro"]),

    ("VACACIONES",        "VACACIONES",     "#0f3460",
        ["id_vacacion"], [],
        ["id_empleado"],
        ["fecha_inicio", "fecha_fin"]),

    ("DIAGNOSTICO",       "DIAGN\u00d3STICO", "#0f3460",
        ["id_diagnostico"], [],
        ["id_paciente", "id_usuario_creacion"],
        ["fecha", "descripcion"]),
]

nuevas = [  # fila nuevas — agregadas en junio
    ("USUARIO",           "USUARIO",        "#2d1b69",
        ["id_usuario"], [],
        [],
        ["username", "password_hash", "nombre_completo", "rol", "activo", "fecha_creacion"]),

    ("AUDITORIA",         "AUDITORIA",      "#2d1b69",
        ["id_auditoria"], [],
        [],
        ["tabla_afectada", "operacion", "descripcion", "fecha_hora"]),
]

phone = [  # fila lateral — compuestas
    ("TELEFONO_EMPLEADO", "TEL\u00c9FONO EMPLEADO", "#16213e",
        ["telefono"],
        ["id_empleado"],
        [],
        []),

    ("TELEFONO_PACIENTE", "TEL\u00c9FONO PACIENTE", "#16213e",
        ["telefono"],
        ["id_paciente"],
        [],
        []),
]

# ──────────────────────────────────────────────────────────────────────
# GENERACIÓN DEL CÓDIGO DOT
# ──────────────────────────────────────────────────────────────────────
dot = []
dot.append("digraph G {")
dot.append('  bgcolor="#1a1a2e";')
dot.append("  rankdir=TB;")
dot.append("  splines=ortho;")
dot.append("  nodesep=0.6;")
dot.append("  ranksep=1.0;")
dot.append("  compound=true;")
dot.append('  node [fontname="Arial", fontsize=10, shape=plain];')
dot.append('  edge [fontname="Arial", color="#5a7a9a", penwidth=1.2, arrowsize=0.6];')
dot.append("")

for (nid, disp, bg, pk, pkfk, fk, norm) in param:
    dot.append(f'  {nid} [label=<{make_label(disp, bg, pk, pkfk, fk, norm)}>];')
dot.append("")

for (nid, disp, bg, pk, pkfk, fk, norm) in main:
    dot.append(f'  {nid} [label=<{make_label(disp, bg, pk, pkfk, fk, norm)}>];')
dot.append("")

for (nid, disp, bg, pk, pkfk, fk, norm) in dep:
    dot.append(f'  {nid} [label=<{make_label(disp, bg, pk, pkfk, fk, norm)}>];')
dot.append("")

for (nid, disp, bg, pk, pkfk, fk, norm) in phone:
    dot.append(f'  {nid} [label=<{make_label(disp, bg, pk, pkfk, fk, norm)}>];')
dot.append("")

for (nid, disp, bg, pk, pkfk, fk, norm) in nuevas:
    dot.append(f'  {nid} [label=<{make_label(disp, bg, pk, pkfk, fk, norm)}>];')
dot.append("")

# ── Filas (rank same) ──
dot.append("  { rank=same; MUNICIPIO; PROFESION; ESPECIALIDAD; TIPO_MEDICO; ENFERMEDAD; }")
dot.append("  { rank=same; EMPLEADO; MEDICO; }")
dot.append("  { rank=same; PACIENTE; HORARIO; VACACIONES; PERIODO_SUSTITUTO; DIAGNOSTICO; }")
dot.append("  { rank=same; TELEFONO_EMPLEADO; TELEFONO_PACIENTE; }")
dot.append("  { rank=same; USUARIO; AUDITORIA; }")
dot.append("")

# ── Flechas FK → PK (sin texto) ──
dot.append("  // PARAMÉTRICAS → nadie (son origen)")
dot.append("")
dot.append("  // PRINCIPALES → PARAMÉTRICAS")
dot.append("  EMPLEADO -> MUNICIPIO;")
dot.append("  EMPLEADO -> PROFESION;")
dot.append("")
dot.append("  MEDICO -> EMPLEADO;")
dot.append("  MEDICO -> TIPO_MEDICO;")
dot.append("  MEDICO -> ESPECIALIDAD;")
dot.append("")
dot.append("  // DEPENDIENTES → PRINCIPALES / PARAMÉTRICAS")
dot.append("  PACIENTE -> MUNICIPIO;")
dot.append("  PACIENTE -> MEDICO;")
dot.append("  HORARIO -> MEDICO;")
dot.append("  VACACIONES -> EMPLEADO;")
dot.append("  PERIODO_SUSTITUTO -> MEDICO;")
dot.append("  DIAGNOSTICO -> PACIENTE;")
dot.append("")
dot.append("  // TELÉFONOS → PRINCIPALES")
dot.append("  TELEFONO_EMPLEADO -> EMPLEADO;")
dot.append("  TELEFONO_PACIENTE -> PACIENTE;")
dot.append("")
dot.append("  // NUEVAS FK → USUARIO (id_usuario_creacion)")
dot.append("  PACIENTE -> USUARIO;")
dot.append("  DIAGNOSTICO -> USUARIO;")
dot.append("")
dot.append("}")  # fin digraph

dot_source = "\n".join(dot)

# ──────────────────────────────────────────────────────────────────────
# ENVÍO A KROKI Y GUARDADO
# ──────────────────────────────────────────────────────────────────────
try:
    headers = {"Content-Type": "text/plain", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
    req = urllib.request.Request(
        "https://kroki.io/graphviz/png",
        data=dot_source.encode("utf-8"),
        headers=headers,
    )
    resp = urllib.request.urlopen(req, timeout=45)
    png = resp.read()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_path = os.path.join(script_dir, "..", "Diagrama_Relacional_Normalizado.png")
    with open(out_path, "wb") as f:
        f.write(png)
    print(f"OK — {len(png)} bytes -> {out_path}")

except Exception as e:
    print(f"ERROR: {e}")
