# -*- coding: utf-8 -*-
"""
Genera los dos diagramas actualizados del Centro de Salud:
1. Diagrama_ER_Oscuro_Normalizado.png (Conceptual)
2. Diagrama_Relacional_Normalizado.png (Fisico)
Incluye las tablas nuevas: usuario, enfermedad, auditoria y columnas id_usuario_creacion.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
import numpy as np

OUTPUT = r"C:\Users\diego\Downloads\Telegram Desktop\proyecto final\proyecto final"

# ============================================================
# DIAGRAMA ENTIDAD-RELACION CONCEPTUAL
# ============================================================
def draw_er_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(20, 14))
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 14)
    ax.axis("off")
    
    title = "Diagrama Entidad-Relación Conceptual — Centro de Salud"
    ax.text(10, 13.5, title, ha="center", va="center", fontsize=14, fontweight="bold",
            color="#f5c842", fontfamily="sans-serif")
    
    # Position map: {name: (x, y, width, height)}
    entities = {}
    
    # Catálogos (left column)
    y_start = 12
    catalogs = [
        ("MUNICIPIO", ["id_municipio (PK)", "nombre"], 1.5, y_start),
        ("ESPECIALIDAD", ["id_especialidad (PK)", "nombre"], 1.5, y_start - 1.8),
        ("TIPO_MEDICO", ["id_tipo (PK)", "nombre"], 1.5, y_start - 3.6),
        ("PROFESION", ["id_profesion (PK)", "nombre"], 1.5, y_start - 5.4),
    ]
    
    # Personal (middle-left)
    personal = [
        ("EMPLEADO", ["id_empleado (PK)", "id_municipio (FK)", "id_profesion (FK)", "nombre", "direccion"], 5.5, y_start),
        ("MEDICO", ["id_empleado (PK/FK)", "num_licencia", "id_tipo (FK)", "id_especialidad (FK)"], 8.5, y_start),
        ("TEL_EMPLEADO", ["id_empleado (PK/FK)", "telefono (PK)"], 5.5, y_start - 2.8),
        ("HORARIO", ["id_horario (PK)", "id_empleado_medico (FK)", "dia_semana", "hora_inicio", "hora_fin"], 8.5, y_start - 2.8),
        ("PERIODO_SUSTITUTO", ["id_periodo (PK)", "id_empleado_medico (FK)", "fecha_ingreso", "fecha_retiro"], 8.5, y_start - 5.2),
        ("VACACIONES", ["id_vacacion (PK)", "id_empleado (FK)", "fecha_inicio", "fecha_fin"], 5.5, y_start - 5.2),
    ]
    
    # Pacientes (right)
    pacientes = [
        ("PACIENTE", ["id_paciente (PK)", "id_municipio (FK)", "id_empleado_medico (FK)", "id_usuario_creacion (FK)", "nombre", "direccion"], 12, y_start),
        ("TEL_PACIENTE", ["id_paciente (PK/FK)", "telefono (PK)"], 12, y_start - 3.5),
        ("DIAGNOSTICO", ["id_diagnostico (PK)", "id_paciente (FK)", "id_usuario_creacion (FK)", "fecha", "descripcion"], 15, y_start),
        ("ENFERMEDAD", ["id_enfermedad (PK)", "nombre"], 15, y_start - 3.5),
    ]
    
    # Nuevas tablas (bottom)
    nuevas = [
        ("USUARIO", ["id_usuario (PK)", "username", "password_hash", "nombre_completo", "rol", "activo", "fecha_creacion"], 12, y_start - 6.5),
        ("AUDITORIA", ["id_auditoria (PK)", "tabla_afectada", "operacion", "descripcion", "fecha_hora"], 15, y_start - 6.5),
    ]
    
    def draw_entity(ax, name, attrs, x, y, weak=False):
        """Dibuja una entidad como caja con atributos."""
        line_h = 0.35
        box_w = 3.0
        box_h = 0.5 + len(attrs) * line_h + 0.3
        
        color = "#f5c842"
        if weak:
            color = "#ff7b72"
            ls = "dashed"
        else:
            ls = "solid"
        
        # Entity box
        rect = mpatches.FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                                        boxstyle="round,pad=0.1",
                                        facecolor="#161b22", edgecolor=color,
                                        linewidth=2, linestyle=ls)
        ax.add_patch(rect)
        
        # Entity name
        ax.text(x, y + box_h/2 - 0.35, name, ha="center", va="center", fontsize=10,
                fontweight="bold", color=color, fontfamily="sans-serif")
        
        # Separator line
        ax.plot([x - box_w/2 + 0.2, x + box_w/2 - 0.2],
                [y + box_h/2 - 0.55, y + box_h/2 - 0.55],
                color=color, linewidth=1)
        
        # Attributes
        for i, attr in enumerate(attrs):
            y_pos = y + box_h/2 - 0.7 - i * line_h
            if "PK" in attr or "PK/FK" in attr:
                c = "#f5c842"
            elif "FK" in attr:
                c = "#58a6ff"
            else:
                c = "#8b949e"
            ax.text(x, y_pos, attr, ha="center", va="center", fontsize=7.5,
                    color=c, fontfamily="sans-serif")
        
        return box_w, box_h
    
    # Draw all entities
    all_entities = catalogs + personal + pacientes + nuevas
    entity_positions = {}
    
    for name, attrs, x, y in all_entities:
        weak = name in ["HORARIO", "PERIODO_SUSTITUTO", "VACACIONES", "DIAGNOSTICO"]
        draw_entity(ax, name, attrs, x, y, weak)
        entity_positions[name] = (x, y)
    
    # Draw relationships (lines between entities)
    def draw_rel(ax, from_name, to_name, label="", color="#58a6ff", style="solid"):
        if from_name not in entity_positions or to_name not in entity_positions:
            return
        x1, y1 = entity_positions[from_name]
        x2, y2 = entity_positions[to_name]
        
        ls = "--" if style == "dashed" else "-"
        lw = 1.5 if style == "dashed" else 1.0
        
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, linestyle=ls, lw=lw))
        
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.15, label, ha="center", va="bottom", fontsize=6.5,
                    color=color, fontfamily="sans-serif",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#0d1117",
                              edgecolor="none", alpha=0.8))
    
    # Relationships: Catalogs -> Personal
    draw_rel(ax, "MUNICIPIO", "EMPLEADO", "1:N")
    draw_rel(ax, "PROFESION", "EMPLEADO", "1:N")
    draw_rel(ax, "TIPO_MEDICO", "MEDICO", "1:N")
    draw_rel(ax, "ESPECIALIDAD", "MEDICO", "1:N")
    
    # ISA between EMPLEADO and MEDICO
    x1, y1 = entity_positions["EMPLEADO"]
    x2, y2 = entity_positions["MEDICO"]
    # Draw triangle ISA
    isa_x = (x1 + x2) / 2
    isa_y = (y1 + y2) / 2
    tri = plt.Polygon([[isa_x, isa_y+0.25], [isa_x-0.3, isa_y-0.25], [isa_x+0.3, isa_y-0.25]],
                      facecolor="#f5c842", edgecolor="#f5c842")
    ax.add_patch(tri)
    ax.text(isa_x, isa_y, "ISA", ha="center", va="center", fontsize=6, fontweight="bold",
            color="black", fontfamily="sans-serif")
    # Lines from triangle to entities
    ax.plot([x1+1.2, isa_x-0.15], [y1, isa_y+0.1], color="#f5c842", linewidth=1.5, linestyle="--")
    ax.plot([isa_x+0.15, x2-1.2], [isa_y+0.1, y2], color="#f5c842", linewidth=1.5)
    
    # Personal relationships
    draw_rel(ax, "EMPLEADO", "TEL_EMPLEADO", "1:N")
    draw_rel(ax, "EMPLEADO", "VACACIONES", "1:N", style="dashed", color="#ff7b72")
    draw_rel(ax, "MEDICO", "HORARIO", "1:N", style="dashed", color="#ff7b72")
    draw_rel(ax, "MEDICO", "PERIODO_SUSTITUTO", "1:N", style="dashed", color="#ff7b72")
    
    # Paciente relationships
    draw_rel(ax, "MUNICIPIO", "PACIENTE", "1:N")
    draw_rel(ax, "MEDICO", "PACIENTE", "1:N")
    draw_rel(ax, "PACIENTE", "TEL_PACIENTE", "1:N")
    draw_rel(ax, "PACIENTE", "DIAGNOSTICO", "1:N", style="dashed", color="#ff7b72")
    
    # NEW: Usuario relationships
    draw_rel(ax, "USUARIO", "PACIENTE", "1:N (creación)", color="#7ee787", style="dashed")
    draw_rel(ax, "USUARIO", "DIAGNOSTICO", "1:N (creación)", color="#7ee787", style="dashed")
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor="#161b22", edgecolor="#f5c842", label="Entidad fuerte"),
        mpatches.Patch(facecolor="#161b22", edgecolor="#ff7b72", linestyle="dashed", label="Entidad débil"),
        plt.Line2D([0], [0], color="#7ee787", linestyle="--", label="Relación nueva (usuario)"),
        plt.Line2D([0], [0], color="#ff7b72", linestyle="--", label="Relación débil"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=7,
              facecolor="#161b22", edgecolor="#30363d", labelcolor="white")
    
    plt.tight_layout()
    path = OUTPUT + "/Diagrama_ER_Oscuro_Normalizado.png"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="#0d1117")
    plt.close()
    print(f"ER Diagram saved: {path}")


# ============================================================
# DIAGRAMA RELACIONAL FISICO
# ============================================================
def draw_relational_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(22, 16))
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.axis("off")
    
    title = "Diagrama Relacional Físico — Centro de Salud (16 tablas)"
    ax.text(11, 15.5, title, ha="center", va="center", fontsize=14, fontweight="bold",
            color="#f5c842", fontfamily="sans-serif")
    
    # Table definitions with columns
    tables = {
        "MUNICIPIO": [
            ("PK  id_municipio", "INT AUTO_INC"),
            ("    nombre", "VARCHAR(100) NOT NULL"),
        ],
        "ESPECIALIDAD": [
            ("PK  id_especialidad", "INT AUTO_INC"),
            ("    nombre", "VARCHAR(100) NOT NULL"),
        ],
        "TIPO_MEDICO": [
            ("PK  id_tipo", "INT AUTO_INC"),
            ("    nombre", "VARCHAR(50) NOT NULL"),
        ],
        "PROFESION": [
            ("PK  id_profesion", "INT AUTO_INC"),
            ("    nombre", "VARCHAR(100) NOT NULL"),
        ],
        "EMPLEADO": [
            ("PK  id_empleado", "INT AUTO_INC"),
            ("FK  id_municipio", "INT"),
            ("FK  id_profesion", "INT"),
            ("    nombre", "VARCHAR(120) NOT NULL"),
            ("    direccion", "VARCHAR(160) NOT NULL"),
        ],
        "MEDICO": [
            ("PK  id_empleado", "INT (FK)"),
            ("    num_licencia", "VARCHAR(50) UNIQUE"),
            ("FK  id_tipo", "INT"),
            ("FK  id_especialidad", "INT"),
        ],
        "TEL_EMPLEADO": [
            ("PK  id_empleado", "INT (FK)"),
            ("PK  telefono", "VARCHAR(20)"),
        ],
        "HORARIO": [
            ("PK  id_horario", "INT AUTO_INC"),
            ("FK  id_empleado_medico", "INT"),
            ("    dia_semana", "ENUM NOT NULL"),
            ("    hora_inicio", "TIME NOT NULL"),
            ("    hora_fin", "TIME NOT NULL"),
        ],
        "PERIODO_SUSTITUTO": [
            ("PK  id_periodo", "INT AUTO_INC"),
            ("FK  id_empleado_medico", "INT"),
            ("    fecha_ingreso", "DATE NOT NULL"),
            ("    fecha_retiro", "DATE NULL"),
        ],
        "VACACIONES": [
            ("PK  id_vacacion", "INT AUTO_INC"),
            ("FK  id_empleado", "INT"),
            ("    fecha_inicio", "DATE NOT NULL"),
            ("    fecha_fin", "DATE NOT NULL"),
        ],
        "USUARIO": [
            ("PK  id_usuario", "INT AUTO_INC"),
            ("    username", "VARCHAR(50) UNIQUE"),
            ("    password_hash", "VARCHAR(64) NOT NULL"),
            ("    nombre_completo", "VARCHAR(120) NOT NULL"),
            ("    rol", "ENUM NOT NULL"),
            ("    activo", "TINYINT DEFAULT 1"),
            ("    fecha_creacion", "DATETIME DEFAULT NOW"),
        ],
        "PACIENTE": [
            ("PK  id_paciente", "INT AUTO_INC"),
            ("FK  id_municipio", "INT"),
            ("FK  id_empleado_medico", "INT"),
            ("[N] FK  id_usuario_creacion", "INT DEFAULT NULL"),
            ("    nombre", "VARCHAR(120) NOT NULL"),
            ("    direccion", "VARCHAR(160) NOT NULL"),
        ],
        "TEL_PACIENTE": [
            ("PK  id_paciente", "INT (FK)"),
            ("PK  telefono", "VARCHAR(20)"),
        ],
        "DIAGNOSTICO": [
            ("PK  id_diagnostico", "INT AUTO_INC"),
            ("FK  id_paciente", "INT"),
            ("[N] FK  id_usuario_creacion", "INT DEFAULT NULL"),
            ("    fecha", "DATE NOT NULL"),
            ("    descripcion", "VARCHAR(255) NOT NULL"),
        ],
        "ENFERMEDAD": [
            ("PK  id_enfermedad", "INT AUTO_INC"),
            ("    nombre", "VARCHAR(150) UNIQUE"),
        ],
        "AUDITORIA": [
            ("PK  id_auditoria", "INT AUTO_INC"),
            ("    tabla_afectada", "VARCHAR(50) NOT NULL"),
            ("    operacion", "VARCHAR(20) NOT NULL"),
            ("    descripcion", "VARCHAR(255)"),
            ("    fecha_hora", "TIMESTAMP DEFAULT NOW"),
        ],
    }
    
    # Positions [x_center, y_center] for each table
    positions = {
        # Catalogs (left)
        "MUNICIPIO": [2, 14],
        "ESPECIALIDAD": [2, 12.2],
        "TIPO_MEDICO": [2, 10.4],
        "PROFESION": [2, 8.6],
        
        # Personal (middle-left)
        "EMPLEADO": [6, 14],
        "MEDICO": [6, 11.5],
        "TEL_EMPLEADO": [6, 8.5],
        "HORARIO": [9, 14],
        "PERIODO_SUSTITUTO": [9, 11.5],
        "VACACIONES": [9, 8.5],
        
        # Patients (right)
        "PACIENTE": [13, 14],
        "TEL_PACIENTE": [13, 11.5],
        "DIAGNOSTICO": [16, 14],
        "ENFERMEDAD": [16, 11.5],
        
        # New (bottom)
        "USUARIO": [13, 6.5],
        "AUDITORIA": [16, 6.5],
    }
    
    def draw_table(ax, name, cols, x, y):
        """Draw a table box with columns."""
        line_h = 0.35
        box_w = 3.5
        box_h = 0.6 + len(cols) * line_h + 0.2
        
        # Check if new table or has new columns
        is_new = name in ["USUARIO", "ENFERMEDAD", "AUDITORIA"]
        has_new_cols = any("[N]" in col[0] for col in cols)
        
        if is_new:
            border_color = "#7ee787"
        elif has_new_cols:
            border_color = "#7ee787"
        else:
            border_color = "#f5c842"
        
        # Draw box
        rect = mpatches.FancyBboxPatch((x - box_w/2, y - box_h/2), box_w, box_h,
                                        boxstyle="round,pad=0.08",
                                        facecolor="#161b22", edgecolor=border_color,
                                        linewidth=2)
        ax.add_patch(rect)
        
        # Table name
        name_color = border_color
        ax.text(x, y + box_h/2 - 0.3, name, ha="center", va="center", fontsize=9,
                fontweight="bold", color=name_color, fontfamily="sans-serif")
        
        # Separator
        ax.plot([x - box_w/2 + 0.2, x + box_w/2 - 0.2],
                [y + box_h/2 - 0.5, y + box_h/2 - 0.5],
                color=border_color, linewidth=1)
        
        # Columns
        for i, (col_name, col_type) in enumerate(cols):
            y_pos = y + box_h/2 - 0.65 - i * line_h
            
            # Determine color based on prefix
            if "[N]" in col_name:
                c = "#7ee787"  # green for new
            elif col_name.startswith("PK") and "FK" in col_name:
                c = "#ff7b72"  # red for PK+FK
            elif col_name.startswith("PK"):
                c = "#f5c842"  # gold for PK
            elif "FK" in col_name:
                c = "#58a6ff"  # blue for FK
            else:
                c = "#8b949e"  # gray for others
            
            ax.text(x - box_w/2 + 0.25, y_pos, col_name, ha="left", va="center",
                    fontsize=6.5, color=c, fontfamily="monospace")
            ax.text(x + box_w/2 - 0.25, y_pos, col_type, ha="right", va="center",
                    fontsize=5.5, color="#484f58", fontfamily="monospace")
    
    # Draw all tables
    for name, cols in tables.items():
        x, y = positions[name]
        draw_table(ax, name, cols, x, y)
    
    # Group labels
    def draw_group_label(ax, text, x, y, w, h):
        rect = mpatches.FancyBboxPatch((x, y), w, h,
                                        boxstyle="round,pad=0.05",
                                        facecolor="none", edgecolor="#30363d",
                                        linewidth=1, linestyle="--")
        ax.add_patch(rect)
        ax.text(x + w/2, y + h + 0.2, text, ha="center", va="bottom", fontsize=7,
                color="#8b949e", fontfamily="sans-serif", style="italic")
    
    # Draw FK relationships
    def draw_fk(ax, from_t, to_t, color="#58a6ff", style="solid", label=""):
        if from_t not in positions or to_t not in positions:
            return
        x1, y1 = positions[from_t]
        x2, y2 = positions[to_t]
        
        ls = "--" if style == "dashed" else "-"
        lw = 1
        
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color=color, linestyle=ls, lw=lw,
                                    connectionstyle="arc3,rad=0.1"))
        if label:
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            ax.text(mx, my + 0.2, label, ha="center", va="bottom", fontsize=5.5,
                    color=color, fontfamily="sans-serif",
                    bbox=dict(boxstyle="round,pad=0.1", facecolor="#0d1117",
                              edgecolor="none", alpha=0.7))
    
    # FK edges
    draw_fk(ax, "EMPLEADO", "MUNICIPIO", label="id_municipio", color="#58a6ff")
    draw_fk(ax, "EMPLEADO", "PROFESION", label="id_profesion", color="#58a6ff")
    draw_fk(ax, "MEDICO", "EMPLEADO", label="id_empleado", color="#f5c842")
    draw_fk(ax, "MEDICO", "TIPO_MEDICO", label="id_tipo", color="#58a6ff")
    draw_fk(ax, "MEDICO", "ESPECIALIDAD", label="id_especialidad", color="#58a6ff")
    draw_fk(ax, "TEL_EMPLEADO", "EMPLEADO", label="id_empleado", color="#58a6ff")
    draw_fk(ax, "HORARIO", "EMPLEADO", label="id_empleado_medico", color="#58a6ff")
    draw_fk(ax, "PERIODO_SUSTITUTO", "EMPLEADO", label="id_empleado_medico", color="#58a6ff")
    draw_fk(ax, "VACACIONES", "EMPLEADO", label="id_empleado", color="#58a6ff")
    draw_fk(ax, "PACIENTE", "MUNICIPIO", label="id_municipio", color="#58a6ff")
    draw_fk(ax, "PACIENTE", "EMPLEADO", label="id_empleado_medico", color="#58a6ff")
    draw_fk(ax, "PACIENTE", "USUARIO", label="id_usuario_creacion", color="#7ee787", style="dashed")
    draw_fk(ax, "TEL_PACIENTE", "PACIENTE", label="id_paciente", color="#58a6ff")
    draw_fk(ax, "DIAGNOSTICO", "PACIENTE", label="id_paciente", color="#58a6ff")
    draw_fk(ax, "DIAGNOSTICO", "USUARIO", label="id_usuario_creacion", color="#7ee787", style="dashed")
    
    # Legend
    legend_elements = [
        mpatches.Patch(facecolor="#161b22", edgecolor="#f5c842", label="Tabla original"),
        mpatches.Patch(facecolor="#161b22", edgecolor="#7ee787", label="Tabla o columna NUEVA"),
        plt.Line2D([0], [0], color="#7ee787", linestyle="--", linewidth=2, label="FK nueva (usuario)"),
        plt.Line2D([0], [0], color="#58a6ff", linewidth=1.5, label="FK existente"),
    ]
    ax.legend(handles=legend_elements, loc="lower left", fontsize=7,
              facecolor="#161b22", edgecolor="#30363d", labelcolor="white")
    
    plt.tight_layout()
    path = OUTPUT + "/Diagrama_Relacional_Normalizado.png"
    plt.savefig(path, dpi=200, bbox_inches="tight", facecolor="#0d1117")
    plt.close()
    print(f"Relational Diagram saved: {path}")


if __name__ == "__main__":
    print("Generando diagramas actualizados...")
    draw_er_diagram()
    draw_relational_diagram()
    print("Listo! Ambos diagramas generados con las tablas nuevas:")
    print("  - USUARIO")
    print("  - ENFERMEDAD")
    print("  - AUDITORIA")
    print("  - id_usuario_creacion en PACIENTE y DIAGNOSTICO")
