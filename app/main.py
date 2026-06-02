# -*- coding: utf-8 -*-
"""
main.py - VitalCare Centro de Salud
Aplicación Streamlit con login, roles, tema oscuro,
gestión de pacientes, diagnósticos, horarios, vacaciones,
usuarios, historial médico y reportes.
"""

import streamlit as st
from datetime import date, time

from db import fetch_options, test_connection
from reports import (
    resumen_dashboard,
    agenda_hoy,
    agenda_por_dia,
    agenda_semanal,
    directorio_medicos,
    buscar_pacientes,
    ultimos_diagnosticos,
    listado_vacaciones,
    pacientes_por_especialidad,
    medicos_disponibles_por_especialidad,
    pacientes_por_diagnostico,
    vacaciones_medicos_intervalo,
)
from auth import (
    login_required,
    sesion_activa,
    mostrar_info_usuario,
    tiene_rol,
    es_admin,
    usuario_actual,
    hash_password,
    listar_usuarios,
    crear_usuario,
    actualizar_usuario,
    cambiar_password,
)
import crud as _crud
from crud import (
    opciones_municipios,
    opciones_medicos,
    opciones_empleados,
    opciones_pacientes,
    opciones_diagnosticos,
    opciones_horarios,
    opciones_vacaciones,
    obtener_paciente,
    obtener_diagnostico,
    crear_paciente,
    actualizar_paciente,
    eliminar_paciente,
    crear_diagnostico,
    actualizar_diagnostico,
    eliminar_diagnostico,
    crear_horario,
    eliminar_horario,
    crear_vacacion,
    eliminar_vacacion,
)

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
st.set_page_config(
    page_title="VitalCare Centro de Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# TEMA OSCURO — "Noche de Esperanza"
# Fondo oscuro profundo, acentos en dorado (esperanza) y
# detalles en cian/verde azulado (confianza).
# ============================================================
def aplicar_tema_oscuro():
    st.markdown(
        """
        <style>
        /* === BASE === */
        .stApp {
            background: #0d1117 !important;
            color: #e6edf3 !important;
        }

        .main .block-container {
            max-width: 1200px;
            padding-top: 1.2rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #f0e6d3 !important;
            letter-spacing: -0.02em;
        }

        p, label, .stMarkdown, .stText, span, div:not([data-testid]) {
            color: #c9d1d9 !important;
        }

        /* === KEYLINE & CONTAINERS === */
        .st-emotion-cache-1wrcr25, .st-emotion-cache-1r4qj8v {
            background: transparent !important;
        }

        /* === SIDEBAR === */
        section[data-testid="stSidebar"] {
            background: #161b22 !important;
            border-right: 1px solid #30363d !important;
        }

        section[data-testid="stSidebar"] * {
            color: #c9d1d9 !important;
        }

        section[data-testid="stSidebar"] label {
            color: #8b949e !important;
        }

        /* Sidebar brand */
        .sidebar-brand {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            border: 1px solid #f5c84233;
            border-radius: 18px;
            padding: 18px 17px;
            margin-bottom: 16px;
            box-shadow: 0 8px 24px rgba(245, 200, 66, 0.08);
        }

        .sidebar-brand h2 {
            color: #f5c842 !important;
            margin: 0 !important;
            font-size: 1.4rem;
        }

        .sidebar-brand p {
            color: #8b949e !important;
            margin: 4px 0 0 0 !important;
            font-size: 0.85rem;
        }

        /* === PORTAL HEADER === */
        .portal-header {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 40%, #0f3460 100%);
            border: 1px solid #f5c84233;
            border-radius: 22px;
            padding: 28px 32px;
            box-shadow: 0 12px 32px rgba(245, 200, 66, 0.06);
            margin-bottom: 22px;
            position: relative;
            overflow: hidden;
        }

        .portal-header::before {
            content: "";
            position: absolute;
            width: 300px;
            height: 300px;
            right: -100px;
            top: -120px;
            background: radial-gradient(circle, rgba(245,200,66,0.06) 0%, transparent 70%);
            border-radius: 50%;
        }

        .portal-header h1 {
            color: #f5c842 !important;
            font-size: 2.1rem;
            font-weight: 850;
            margin: 0 0 8px 0;
        }

        .portal-header p {
            color: #8b949e !important;
            max-width: 800px;
            font-size: 1rem;
            margin: 0;
        }

        .badge {
            display: inline-block;
            margin-top: 16px;
            margin-right: 8px;
            padding: 6px 14px;
            border-radius: 999px;
            background: rgba(245, 200, 66, 0.1);
            border: 1px solid rgba(245, 200, 66, 0.25);
            color: #f5c842 !important;
            font-weight: 700;
            font-size: 0.8rem;
        }

        /* === TARJETAS === */
        .metric-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 18px;
            padding: 20px 22px;
            height: 100%;
            transition: border-color 0.2s;
        }

        .metric-card:hover {
            border-color: #f5c84255;
        }

        .metric-card .label {
            color: #8b949e !important;
            font-size: 0.78rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
        }

        .metric-card .value {
            color: #f5c842 !important;
            font-size: 2rem;
            font-weight: 850;
            margin-top: 2px;
        }

        .metric-card .hint {
            color: #6e7681 !important;
            font-size: 0.82rem;
        }

        .module-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 18px;
            padding: 20px 22px;
            height: 100%;
            transition: border-color 0.2s;
        }

        .module-card:hover {
            border-color: #f5c84255;
        }

        .module-card h3 {
            color: #f0e6d3 !important;
            margin: 0 0 8px 0;
            font-weight: 850;
            font-size: 1rem;
        }

        .module-card p {
            color: #8b949e !important;
            margin: 0;
            font-size: 0.9rem;
        }

        .soft-panel {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 18px;
            padding: 20px 22px;
            margin-bottom: 18px;
        }

        /* === NOTICES === */
        .notice {
            background: #0d1b1e;
            border: 1px solid #f5c84244;
            border-radius: 16px;
            padding: 14px 18px;
            color: #f5c842 !important;
            margin-bottom: 16px;
        }

        .danger {
            background: #2d0a0e;
            border: 1px solid #e9456066;
            border-radius: 16px;
            padding: 14px 18px;
            color: #e94560 !important;
            margin-bottom: 16px;
        }

        /* === FORMULARIOS === */
        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextArea"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTimeInput"] label,
        div[data-testid="stSelectbox"] label {
            color: #c9d1d9 !important;
            font-weight: 700 !important;
        }

        input, textarea,
        div[data-baseweb="input"],
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"],
        div[data-baseweb="textarea"] textarea {
            background-color: #0d1117 !important;
            color: #e6edf3 !important;
            -webkit-text-fill-color: #e6edf3 !important;
            border-color: #30363d !important;
            caret-color: #f5c842 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #0d1117 !important;
            color: #e6edf3 !important;
            border-color: #30363d !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input {
            color: #e6edf3 !important;
            -webkit-text-fill-color: #e6edf3 !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            background-color: #161b22 !important;
            color: #e6edf3 !important;
        }

        ul[role="listbox"] li,
        div[role="option"] {
            color: #e6edf3 !important;
            background-color: #161b22 !important;
        }

        ul[role="listbox"] li:hover,
        div[role="option"]:hover {
            background-color: #1f2937 !important;
        }

        /* === BOTONES === */
        .stButton > button {
            background: #f5c842 !important;
            color: #0d1117 !important;
            border: 0 !important;
            border-radius: 12px !important;
            font-weight: 800 !important;
            padding: 0.5rem 1rem !important;
            transition: all 0.2s;
        }

        .stButton > button:hover {
            background: #e6b800 !important;
            color: #0d1117 !important;
            box-shadow: 0 4px 16px rgba(245, 200, 66, 0.3);
        }

        .stButton > button[kind="secondary"] {
            background: transparent !important;
            color: #f5c842 !important;
            border: 1px solid #f5c84266 !important;
        }

        .stButton > button[kind="secondary"]:hover {
            background: rgba(245, 200, 66, 0.1) !important;
        }

        /* === DATAFRAME === */
        div[data-testid="stDataFrame"] {
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #30363d;
        }

        div[data-testid="stDataFrame"] th {
            background: #1c2333 !important;
            color: #f5c842 !important;
        }

        div[data-testid="stDataFrame"] td {
            background: #0d1117 !important;
            color: #c9d1d9 !important;
        }

        /* === TABS === */
        div[data-baseweb="tab-list"] {
            gap: 4px;
            background: transparent;
        }

        div[data-baseweb="tab"] {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 12px 12px 0 0;
            color: #8b949e;
            font-weight: 700;
        }

        div[data-baseweb="tab"][aria-selected="true"] {
            background: #0d1117;
            border-color: #f5c842;
            color: #f5c842;
            border-bottom-color: #0d1117;
        }

        /* === RADIO BUTTONS === */
        div[data-testid="stRadio"] label {
            color: #c9d1d9 !important;
        }

        div[data-testid="stRadio"] label:hover {
            color: #f5c842 !important;
        }

        /* === MISC === */
        hr {
            border-color: #30363d !important;
        }

        .stSuccess {
            background: #0d2818 !important;
            border-color: #4ade8055 !important;
            color: #4ade80 !important;
        }

        .stError {
            background: #2d0a0e !important;
            border-color: #e9456066 !important;
            color: #e94560 !important;
        }

        .stWarning {
            background: #1a1400 !important;
            border-color: #f5c84244 !important;
            color: #f5c842 !important;
        }

        .stInfo {
            background: #0d1b2a !important;
            border-color: #38bdf855 !important;
            color: #38bdf8 !important;
        }

        .stProgress > div > div {
            background-color: #f5c842 !important;
        }

        /* ===== LOGIN / USER BAR ===== */
        .user-bar {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 14px;
            padding: 8px 18px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .user-bar span {
            color: #c9d1d9 !important;
            font-size: 0.9rem;
        }

        .user-bar .user-name {
            color: #f5c842 !important;
            font-weight: 700;
        }

        .login-box {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 22px;
            padding: 2.5rem 2rem;
            max-width: 420px;
            margin: 3rem auto;
        }

        .login-box h3 {
            color: #f5c842 !important;
            text-align: center;
            margin-bottom: 1.5rem;
        }

        /* Scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #0d1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #30363d;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #f5c84266;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def title(text, subtitle=""):
    st.markdown(f"<div class='section-title' style='color:#f0e6d3!important;font-size:1.55rem;font-weight:850;margin:0.4rem 0 0.15rem 0;'>{text}</div>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<div style='color:#8b949e!important;margin-bottom:1.1rem;'>{subtitle}</div>", unsafe_allow_html=True)


def metric_card(label, value, hint):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="label">{label}</div>
            <div class="value">{value}</div>
            <div class="hint">{hint}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def module_card(title_, body):
    st.markdown(
        f"""
        <div class="module-card">
            <h3>{title_}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def show_table(df, empty_message="No hay registros para mostrar."):
    if df is None or df.empty:
        st.info(empty_message)
    else:
        st.dataframe(df, use_container_width=True, hide_index=True)


def get_especialidades():
    return fetch_options("SELECT nombre FROM especialidad ORDER BY nombre;")


def pair_select(label, pairs, key=None, selected_id=None):
    if not pairs:
        st.warning("No hay opciones disponibles.")
        return None

    labels = {item[0]: item[1] for item in pairs}
    ids = list(labels.keys())

    index = 0
    if selected_id in ids:
        index = ids.index(selected_id)

    return st.selectbox(
        label,
        ids,
        index=index,
        format_func=lambda x: labels[x],
        key=key
    )


# ============================================================
# HEADER
# ============================================================
def header():
    st.markdown(
        """
        <div class="portal-header">
            <h1>🏥 VitalCare Centro de Salud</h1>
            <p>
                Portal administrativo para gestionar pacientes, diagnósticos, horarios, vacaciones,
                usuarios y reportes del centro de salud.
            </p>
            <span class="badge">✦ MySQL conectado</span>
            <span class="badge">✦ Gestión clínica</span>
            <span class="badge">✦ Reportes operativos</span>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# INICIO — DASHBOARD
# ============================================================
def pagina_inicio():
    title("Panel general", "Vista rápida del estado operativo y clínico del centro de salud.")

    try:
        data = _crud.resumen_centro().iloc[0]

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            metric_card("Pacientes", int(data["total_pacientes"]), "Registrados en el sistema")
        with c2:
            metric_card("Médicos", int(data["total_medicos"]), "Personal médico")
        with c3:
            metric_card("Diagnósticos", int(data["total_diagnosticos"]), "Registros clínicos")
        with c4:
            metric_card("Usuarios", int(data["total_usuarios"]), "Cuentas activas")
    except Exception as e:
        st.error("No se pudo cargar el panel general.")

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        module_card("📋 Gestión de pacientes", "Registrar, actualizar y consultar pacientes del centro.")
    with c2:
        module_card("🩺 Gestión de diagnósticos", "Registrar diagnósticos clínicos con enfermedades predefinidas.")
    with c3:
        module_card("📊 Gestión médica", "Historial de pacientes, horarios, vacaciones y médicos.")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
        st.subheader("📅 Agenda de hoy")
        show_table(agenda_hoy(), "No hay consultas programadas para hoy.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
        st.subheader("🕐 Últimos diagnósticos")
        show_table(ultimos_diagnosticos(6), "No hay diagnósticos registrados.")
        st.markdown("</div>", unsafe_allow_html=True)


# ============================================================
# GESTIÓN DE PACIENTES
# ============================================================
def pagina_pacientes():
    title("Gestión de pacientes", "Registrar, consultar, actualizar y eliminar pacientes.")

    st.markdown("<div class='notice'>ℹ️ Los pacientes nuevos se registran con el usuario que inició sesión.</div>", unsafe_allow_html=True)

    st.subheader("🔍 Consulta de pacientes")
    busqueda = st.text_input("Buscar paciente", placeholder="Nombre, médico, especialidad, municipio o ID")
    show_table(buscar_pacientes(busqueda.strip()), "No se encontraron pacientes.")

    st.divider()
    st.subheader("Operaciones")

    operacion = st.selectbox(
        "Operación sobre pacientes",
        ["Registrar paciente", "Actualizar paciente", "Eliminar paciente"],
        key="pacientes_operacion"
    )

    if operacion == "Registrar paciente":
        with st.form("form_crear_paciente"):
            nombre = st.text_input("Nombre completo")
            direccion = st.text_input("Dirección")
            telefono = st.text_input("Teléfono principal (opcional)")
            id_municipio = pair_select("Municipio", opciones_municipios(), key="crear_paciente_municipio")
            id_medico = pair_select("Médico responsable", opciones_medicos(), key="crear_paciente_medico")
            enviar = st.form_submit_button("Guardar paciente")

            if enviar:
                if not nombre.strip() or not direccion.strip() or id_municipio is None or id_medico is None:
                    st.warning("Completa nombre, dirección, municipio y médico.")
                else:
                    try:
                        usuario = usuario_actual()
                        id_usuario = usuario["id_usuario"] if usuario else None
                        nuevo_id = crear_paciente(
                            nombre.strip(), direccion.strip(),
                            id_municipio, id_medico,
                            id_usuario_creacion=id_usuario,
                            telefono=telefono
                        )
                        st.success(f"Paciente registrado correctamente. ID: {nuevo_id}")
                    except Exception as e:
                        st.error("No se pudo registrar el paciente.")
                        st.exception(e)

    elif operacion == "Actualizar paciente":
        id_paciente = pair_select("Paciente a actualizar", opciones_pacientes(), key="actualizar_paciente_select")
        if id_paciente:
            actual = obtener_paciente(id_paciente)
            if actual is not None:
                municipios = opciones_municipios()
                medicos = opciones_medicos()

                with st.form("form_actualizar_paciente"):
                    nombre = st.text_input("Nombre", value=str(actual["nombre"]))
                    direccion = st.text_input("Dirección", value=str(actual["direccion"]))
                    id_municipio = pair_select(
                        "Municipio", municipios,
                        key="actualizar_paciente_municipio",
                        selected_id=int(actual["id_municipio"])
                    )
                    id_medico = pair_select(
                        "Médico responsable", medicos,
                        key="actualizar_paciente_medico",
                        selected_id=int(actual["id_empleado_medico"])
                    )
                    enviar = st.form_submit_button("Actualizar paciente")

                    if enviar:
                        try:
                            actualizar_paciente(id_paciente, nombre.strip(), direccion.strip(), id_municipio, id_medico)
                            st.success("Paciente actualizado correctamente.")
                        except Exception as e:
                            st.error("No se pudo actualizar el paciente.")
                            st.exception(e)

    elif operacion == "Eliminar paciente":
        st.markdown("<div class='danger'>⚠️ Al eliminar un paciente se eliminan también sus teléfonos y diagnósticos asociados.</div>", unsafe_allow_html=True)
        id_paciente = pair_select("Paciente a eliminar", opciones_pacientes(), key="eliminar_paciente_select")
        confirmar = st.checkbox("Confirmo que deseo eliminar este paciente")

        if st.button("Eliminar paciente"):
            if not confirmar:
                st.warning("Marca la casilla de confirmación.")
            else:
                try:
                    eliminar_paciente(id_paciente)
                    st.success("Paciente eliminado correctamente.")
                except Exception as e:
                    st.error("No se pudo eliminar el paciente.")
                    st.exception(e)


# ============================================================
# GESTIÓN DE DIAGNÓSTICOS
# ============================================================
def pagina_diagnosticos():
    title("Gestión de diagnósticos", "Registrar, actualizar y eliminar diagnósticos clínicos.")

    st.markdown("<div class='notice'>ℹ️ Cada diagnóstico registra automáticamente el usuario que lo creó.</div>", unsafe_allow_html=True)

    st.subheader("🕐 Últimos diagnósticos")
    show_table(ultimos_diagnosticos(15), "No hay diagnósticos registrados.")

    st.divider()
    st.subheader("Operaciones")

    operacion = st.selectbox(
        "Operación sobre diagnósticos",
        ["Registrar diagnóstico", "Actualizar diagnóstico", "Eliminar diagnóstico"],
        key="diagnosticos_operacion"
    )

    if operacion == "Registrar diagnóstico":
        with st.form("form_crear_diagnostico"):
            id_paciente = pair_select("Paciente", opciones_pacientes(), key="crear_diag_paciente")
            fecha_diag = st.date_input("Fecha", value=date.today())
            enfermedades = _crud.opciones_enfermedades()
            enfermedad_sel = st.selectbox(
                "Enfermedad (predefinida)",
                [""] + [e[1] for e in enfermedades],
                format_func=lambda x: "--- Seleccione una enfermedad ---" if x == "" else x
            )
            descripcion = st.text_area(
                "O escribir diagnóstico manualmente",
                placeholder="Solo si la enfermedad no está en la lista",
                help="Si seleccionaste una enfermedad arriba, este campo es opcional."
            )
            enviar = st.form_submit_button("Guardar diagnóstico")

            if enviar:
                diag_final = enfermedad_sel if enfermedad_sel else (descripcion.strip() if descripcion else "")
                if id_paciente is None or not diag_final:
                    st.warning("Selecciona un paciente y una enfermedad o escribe la descripción.")
                else:
                    try:
                        usuario = usuario_actual()
                        id_usuario = usuario["id_usuario"] if usuario else None
                        nuevo_id = crear_diagnostico(id_paciente, fecha_diag, diag_final, id_usuario_creacion=id_usuario)
                        st.success(f"Diagnóstico registrado correctamente. ID: {nuevo_id}")
                    except Exception as e:
                        st.error("No se pudo registrar el diagnóstico.")
                        st.exception(e)

    elif operacion == "Actualizar diagnóstico":
        id_diag = pair_select("Diagnóstico a actualizar", opciones_diagnosticos(), key="actualizar_diag_select")
        if id_diag:
            actual = obtener_diagnostico(id_diag)
            if actual is not None:
                with st.form("form_actualizar_diagnostico"):
                    fecha_diag = st.date_input("Fecha", value=actual["fecha"])
                    descripcion = st.text_area("Descripción", value=str(actual["descripcion"]))
                    enviar = st.form_submit_button("Actualizar diagnóstico")

                    if enviar:
                        try:
                            actualizar_diagnostico(id_diag, fecha_diag, descripcion.strip())
                            st.success("Diagnóstico actualizado correctamente.")
                        except Exception as e:
                            st.error("No se pudo actualizar el diagnóstico.")
                            st.exception(e)

    elif operacion == "Eliminar diagnóstico":
        id_diag = pair_select("Diagnóstico a eliminar", opciones_diagnosticos(), key="eliminar_diag_select")
        confirmar = st.checkbox("Confirmo que deseo eliminar este diagnóstico")

        if st.button("Eliminar diagnóstico"):
            if not confirmar:
                st.warning("Marca la casilla de confirmación.")
            else:
                try:
                    eliminar_diagnostico(id_diag)
                    st.success("Diagnóstico eliminado correctamente.")
                except Exception as e:
                    st.error("No se pudo eliminar el diagnóstico.")
                    st.exception(e)


# ============================================================
# GESTIÓN MÉDICA — HISTORIAL, ASIGNACIONES
# ============================================================
def pagina_gestion_medica():
    title("Gestión médica", "Historial clínico, asignación de pacientes y directorio médico.")

    tabs = st.tabs(["📋 Historial del paciente", "👨‍⚕️ Médicos y pacientes", "🕐 Horarios", "🏖️ Vacaciones"])

    # ---- TAB 1: HISTORIAL ----
    with tabs[0]:
        st.subheader("Historial clínico completo")
        st.markdown("<div class='notice'>Selecciona un paciente para ver todo su historial de diagnósticos.</div>", unsafe_allow_html=True)

        id_paciente = pair_select("Paciente", opciones_pacientes(), key="historial_paciente_select")
        if id_paciente and st.button("Ver historial completo", key="btn_historial"):
            df_hist = _crud.historial_paciente(id_paciente)
            if df_hist.empty:
                st.info("Este paciente no tiene diagnósticos registrados.")
            else:
                show_table(df_hist, "No hay diagnósticos.")
                st.caption(f"Total de diagnósticos: {len(df_hist)}")

    # ---- TAB 2: MÉDICOS Y PACIENTES ----
    with tabs[1]:
        st.subheader("Pacientes por médico")
        id_medico = pair_select("Médico", opciones_medicos(), key="medico_pacientes_select")
        if id_medico and st.button("Ver pacientes asignados", key="btn_pacientes_x_medico"):
            df_pac = _crud.pacientes_por_medico(id_medico)
            show_table(df_pac, "Este médico no tiene pacientes asignados.")

        st.divider()
        st.subheader("Directorio médico")
        busqueda = st.text_input("Buscar médico", placeholder="Nombre, especialidad, tipo o licencia", key="buscar_medico")
        show_table(directorio_medicos(busqueda.strip()), "No se encontraron médicos.")

    # ---- TAB 3: HORARIOS ----
    with tabs[2]:
        st.subheader("Horarios de consulta")
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        vista = st.selectbox(
            "Vista", ["Agenda semanal completa", "Agenda por día", "Registrar horario", "Eliminar horario"],
            key="horarios_vista"
        )

        if vista == "Agenda semanal completa":
            show_table(agenda_semanal(), "No hay horarios registrados.")
        elif vista == "Agenda por día":
            dia = st.selectbox("Día", dias, key="horario_dia")
            show_table(agenda_por_dia(dia), "No hay horarios para ese día.")
        elif vista == "Registrar horario":
            with st.form("form_crear_horario_gm"):
                id_medico = pair_select("Médico", opciones_medicos(), key="crear_horario_medico_gm")
                dia = st.selectbox("Día de consulta", dias)
                hora_inicio = st.time_input("Hora de inicio", value=time(8, 0))
                hora_fin = st.time_input("Hora de fin", value=time(12, 0))
                enviar = st.form_submit_button("Guardar horario")
                if enviar:
                    if hora_fin <= hora_inicio:
                        st.warning("La hora final debe ser mayor que la hora inicial.")
                    else:
                        try:
                            nuevo_id = crear_horario(id_medico, dia, hora_inicio, hora_fin)
                            st.success(f"Horario registrado. ID: {nuevo_id}")
                        except Exception as e:
                            st.error("No se pudo registrar el horario.")
                            st.exception(e)
        elif vista == "Eliminar horario":
            show_table(agenda_semanal(), "No hay horarios.")
            id_horario = pair_select("Horario a eliminar", opciones_horarios(), key="eliminar_horario_select_gm")
            confirmar = st.checkbox("Confirmo la eliminación", key="confirm_horario")
            if st.button("Eliminar horario") and confirmar:
                try:
                    eliminar_horario(id_horario)
                    st.success("Horario eliminado.")
                except Exception as e:
                    st.error("Error al eliminar.")

    # ---- TAB 4: VACACIONES ----
    with tabs[3]:
        st.subheader("Vacaciones del personal")
        vista_v = st.selectbox(
            "Vista", ["Listado general", "Registrar vacaciones", "Eliminar vacaciones"],
            key="vacaciones_vista"
        )
        if vista_v == "Listado general":
            busqueda = st.text_input("Buscar por empleado", key="buscar_vacaciones")
            show_table(listado_vacaciones(busqueda.strip()), "No hay vacaciones registradas.")
        elif vista_v == "Registrar vacaciones":
            with st.form("form_crear_vacacion_gm"):
                id_empleado = pair_select("Empleado", opciones_empleados(), key="crear_vacacion_empleado_gm")
                fecha_inicio = st.date_input("Fecha inicio", value=date.today())
                fecha_fin = st.date_input("Fecha fin", value=date.today())
                enviar = st.form_submit_button("Guardar vacaciones")
                if enviar:
                    if fecha_fin < fecha_inicio:
                        st.warning("La fecha final debe ser mayor o igual a la inicial.")
                    else:
                        try:
                            nuevo_id = crear_vacacion(id_empleado, fecha_inicio, fecha_fin)
                            st.success(f"Vacaciones registradas. ID: {nuevo_id}")
                        except Exception as e:
                            st.error("Error al registrar.")
                            st.exception(e)
        elif vista_v == "Eliminar vacaciones":
            show_table(listado_vacaciones(), "No hay vacaciones.")
            id_vacacion = pair_select("Periodo a eliminar", opciones_vacaciones(), key="eliminar_vacacion_select_gm")
            confirmar = st.checkbox("Confirmo la eliminación", key="confirm_vacaciones")
            if st.button("Eliminar vacaciones") and confirmar:
                try:
                    eliminar_vacacion(id_vacacion)
                    st.success("Vacaciones eliminadas.")
                except Exception as e:
                    st.error("Error al eliminar.")


# ============================================================
# GESTIÓN DE USUARIOS (SOLO ADMIN)
# ============================================================
def pagina_usuarios():
    if not es_admin():
        st.error("⛔ Acceso restringido. Solo administradores pueden gestionar usuarios.")
        return

    title("Gestión de usuarios", "Crear, modificar y desactivar cuentas del sistema.")

    st.markdown("<div class='notice'>🔐 Panel exclusivo para administradores. Los cambios aplican inmediatamente.</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 Usuarios registrados", "➕ Nuevo usuario"])

    with tab1:
        df_usuarios = _crud.listar_usuarios_completo()
        show_table(df_usuarios, "No hay usuarios registrados.")

        st.divider()
        st.subheader("Editar usuario")

        usuarios_opts = _crud.opciones_usuarios()
        if usuarios_opts:
            id_usuario = pair_select("Seleccionar usuario", usuarios_opts, key="editar_usuario_select")

            if id_usuario:
                user_data = _crud.obtener_usuario(id_usuario)
                if user_data is not None:
                    with st.form("form_editar_usuario"):
                        new_nombre = st.text_input("Nombre completo", value=str(user_data["nombre_completo"]))
                        new_rol = st.selectbox(
                            "Rol",
                            ["admin", "medico", "enfermero", "recepcionista"],
                            index=["admin", "medico", "enfermero", "recepcionista"].index(str(user_data["rol"]))
                        )
                        new_activo = st.checkbox("Usuario activo", value=bool(user_data["activo"]))
                        new_password = st.text_input("Nueva contraseña (dejar vacío para no cambiar)", type="password")

                        if st.form_submit_button("Guardar cambios"):
                            actualizar_usuario(id_usuario, new_nombre.strip(), new_rol, new_activo)
                            if new_password.strip():
                                cambiar_password(id_usuario, new_password.strip())
                            st.success("Usuario actualizado correctamente.")
                            st.rerun()

    with tab2:
        with st.form("form_nuevo_usuario"):
            nuevo_username = st.text_input("Nombre de usuario", placeholder="Ej: dr.pedro")
            nuevo_nombre = st.text_input("Nombre completo", placeholder="Ej: Dr. Pedro Martínez")
            nuevo_password = st.text_input("Contraseña", type="password")
            nuevo_rol = st.selectbox("Rol", ["medico", "enfermero", "recepcionista", "admin"])
            enviar = st.form_submit_button("Crear usuario")

            if enviar:
                if not nuevo_username.strip() or not nuevo_nombre.strip() or not nuevo_password.strip():
                    st.warning("Completa todos los campos.")
                else:
                    try:
                        crear_usuario(
                            nuevo_username.strip(),
                            hash_password(nuevo_password.strip()),
                            nuevo_nombre.strip(),
                            nuevo_rol
                        )
                        st.success(f"Usuario '{nuevo_username}' creado correctamente.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"No se pudo crear el usuario. ¿El username ya existe?")
                        st.exception(e)


# ============================================================
# REPORTES DEL CENTRO
# ============================================================
def pagina_reportes():
    title("Reportes del centro", "Consultas oficiales solicitadas en el enunciado del proyecto.")

    st.markdown(
        "<div class='notice'>📋 Esta sección agrupa los 4 reportes mínimos exigidos para la entrega y sustentación del proyecto.</div>",
        unsafe_allow_html=True
    )

    reporte = st.selectbox(
        "Seleccione el reporte",
        [
            "1. Pacientes por especialidad del médico",
            "2. Médicos disponibles por especialidad",
            "3. Pacientes por diagnóstico",
            "4. Vacaciones de médicos en intervalo",
        ],
        key="reporte_select"
    )

    if reporte == "1. Pacientes por especialidad del médico":
        st.subheader("Pacientes a cargo de médicos según especialidad")
        especialidad = st.selectbox("Especialidad", get_especialidades(), key="r1_especialidad")
        if st.button("Generar reporte", key="r1_btn"):
            show_table(pacientes_por_especialidad(especialidad), "No hay pacientes para esa especialidad.")

    elif reporte == "2. Médicos disponibles por especialidad":
        st.subheader("Médicos disponibles para una especialidad")
        especialidad = st.selectbox("Especialidad", get_especialidades(), key="r2_especialidad")
        if st.button("Generar reporte", key="r2_btn"):
            show_table(medicos_disponibles_por_especialidad(especialidad), "No hay médicos disponibles para esa especialidad.")

    elif reporte == "3. Pacientes por diagnóstico":
        st.subheader("Pacientes diagnosticados con determinada enfermedad")
        texto = st.text_input("Enfermedad o palabra clave", placeholder="Ejemplo: Hipertensión, Diabetes, Asma")
        if st.button("Generar reporte", key="r3_btn"):
            if not texto.strip():
                st.warning("Ingresa una enfermedad o palabra clave.")
            else:
                show_table(pacientes_por_diagnostico(texto.strip()), "No hay pacientes con ese diagnóstico.")

    elif reporte == "4. Vacaciones de médicos en intervalo":
        st.subheader("Médicos con vacaciones en un intervalo")
        c1, c2 = st.columns(2)
        with c1:
            fecha_inicio = st.date_input("Fecha inicial", value=date(2025, 1, 1))
        with c2:
            fecha_fin = st.date_input("Fecha final", value=date(2025, 12, 31))
        if st.button("Generar reporte", key="r4_btn"):
            if fecha_fin < fecha_inicio:
                st.warning("La fecha final no puede ser menor que la inicial.")
            else:
                show_table(vacaciones_medicos_intervalo(fecha_inicio, fecha_fin), "No hay médicos con vacaciones en ese intervalo.")


# ============================================================
# APLICACIÓN PRINCIPAL
# ============================================================

# 1. Aplicar tema oscuro (corre antes que cualquier contenido)
aplicar_tema_oscuro()

# 2. Sidebar
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <h2>✦ VitalCare</h2>
            <p>Centro de Salud</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        if test_connection():
            st.success("✅ Base de datos conectada")
    except Exception as e:
        st.error("❌ No fue posible conectar con MySQL.")
        st.exception(e)
        st.stop()

    # Solo mostrar navegación si hay sesión activa
    if sesion_activa():
        mostrar_info_usuario()
        st.divider()

        opciones_menu = ["🏠 Inicio", "👥 Pacientes", "📋 Diagnósticos", "📊 Gestión médica", "📈 Reportes"]
        if es_admin():
            opciones_menu.append("👤 Usuarios")

        page = st.radio("Menú principal", opciones_menu, key="nav_menu")
        st.divider()
        st.caption("Bases de Datos Avanzadas • 2026")

# 3. Contenido principal
if not sesion_activa():
    # Mostrar login en el área central
    login_required()
else:
    header()

    if page == "🏠 Inicio":
        pagina_inicio()
    elif page == "👥 Pacientes":
        pagina_pacientes()
    elif page == "📋 Diagnósticos":
        pagina_diagnosticos()
    elif page == "📊 Gestión médica":
        pagina_gestion_medica()
    elif page == "👤 Usuarios":
        pagina_usuarios()
    elif page == "📈 Reportes":
        pagina_reportes()
