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
from crud import (
    opciones_municipios,
    opciones_medicos,
    opciones_empleados,
    opciones_pacientes,
    opciones_diagnosticos,
    opciones_horarios,
    opciones_vacaciones,
    opciones_enfermedades,
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


st.set_page_config(
    page_title="VitalCare Centro de Salud",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


def apply_styles():
    st.markdown(
        """
        <style>
        /* =========================
           BASE GENERAL
        ========================== */
        .stApp {
            background: #f5fbfa !important;
            color: #1f2937 !important;
        }

        .main .block-container {
            max-width: 1180px;
            padding-top: 1.4rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3, h4, h5, h6 {
            color: #12343b !important;
            letter-spacing: -0.02em;
        }

        p, label, .stMarkdown, .stText {
            color: #334155 !important;
        }

        /* =========================
           SIDEBAR
        ========================== */
        section[data-testid="stSidebar"] {
            background: #ffffff !important;
            border-right: 1px solid #d9ecea;
        }

        section[data-testid="stSidebar"] * {
            color: #12343b !important;
        }

        .sidebar-brand {
            background: linear-gradient(135deg, #006d77 0%, #0a9396 100%);
            border-radius: 20px;
            padding: 18px 17px;
            margin-bottom: 14px;
            box-shadow: 0 12px 24px rgba(0, 109, 119, .18);
        }

        .sidebar-brand h2,
        .sidebar-brand p {
            color: white !important;
            margin: 0 !important;
        }

        .sidebar-brand p {
            opacity: .9;
            font-size: .9rem;
            margin-top: 4px !important;
        }

        /* =========================
           HEADER TIPO PORTAL
        ========================== */
        .portal-header {
            background: linear-gradient(120deg, #005f73 0%, #0a9396 55%, #16a085 100%);
            border-radius: 26px;
            padding: 30px 34px;
            color: white;
            box-shadow: 0 16px 38px rgba(0, 95, 115, .22);
            margin-bottom: 24px;
            position: relative;
            overflow: hidden;
        }

        .portal-header:after {
            content: "";
            position: absolute;
            width: 280px;
            height: 280px;
            right: -80px;
            top: -90px;
            background: rgba(255,255,255,.15);
            border-radius: 50%;
        }

        .portal-header h1 {
            color: white !important;
            font-size: 2.25rem;
            font-weight: 850;
            margin: 0 0 8px 0;
        }

        .portal-header p {
            color: #eafffb !important;
            max-width: 850px;
            font-size: 1.02rem;
            margin: 0;
        }

        .badge {
            display: inline-block;
            margin-top: 18px;
            margin-right: 8px;
            padding: 7px 13px;
            border-radius: 999px;
            background: rgba(255,255,255,.18);
            border: 1px solid rgba(255,255,255,.28);
            color: white !important;
            font-weight: 700;
            font-size: .86rem;
        }

        /* =========================
           TARJETAS Y PANELES
        ========================== */
        .metric-card {
            background: #ffffff;
            border: 1px solid #d9ecea;
            border-radius: 22px;
            padding: 20px;
            box-shadow: 0 10px 26px rgba(15, 76, 83, .06);
            height: 100%;
        }

        .metric-card .label {
            color: #64748b !important;
            font-size: .82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: .04em;
        }

        .metric-card .value {
            color: #006d77 !important;
            font-size: 2rem;
            font-weight: 850;
            margin-top: 4px;
        }

        .metric-card .hint {
            color: #64748b !important;
            font-size: .86rem;
        }

        .module-card {
            background: #ffffff;
            border: 1px solid #d9ecea;
            border-radius: 22px;
            padding: 20px;
            box-shadow: 0 10px 26px rgba(15, 76, 83, .06);
            height: 100%;
        }

        .module-card h3 {
            color: #12343b !important;
            margin: 0 0 8px 0;
            font-weight: 850;
            font-size: 1.05rem;
        }

        .module-card p {
            color: #64748b !important;
            margin: 0;
            font-size: .92rem;
        }

        .soft-panel {
            background: #ffffff;
            border: 1px solid #d9ecea;
            border-radius: 22px;
            padding: 20px;
            box-shadow: 0 10px 26px rgba(15, 76, 83, .05);
            margin-bottom: 18px;
        }

        .notice {
            background: #e6fffb;
            border: 1px solid #99f6e4;
            border-radius: 18px;
            padding: 14px 16px;
            color: #134e4a !important;
            margin-bottom: 16px;
        }

        .danger {
            background: #fff1f2;
            border: 1px solid #fecdd3;
            border-radius: 18px;
            padding: 14px 16px;
            color: #881337 !important;
            margin-bottom: 16px;
        }

        .section-title {
            color: #12343b !important;
            font-size: 1.55rem;
            font-weight: 850;
            margin: .4rem 0 .15rem 0;
        }

        .section-subtitle {
            color: #64748b !important;
            margin-bottom: 1.1rem;
        }

        /* =========================
           FORMULARIOS: CORRECCIÓN VISUAL
           Evita campos negros y textos invisibles.
        ========================== */
        div[data-testid="stWidgetLabel"] label,
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stTextInput"] label,
        div[data-testid="stTextArea"] label,
        div[data-testid="stDateInput"] label,
        div[data-testid="stTimeInput"] label,
        div[data-testid="stSelectbox"] label {
            color: #334155 !important;
            font-weight: 700 !important;
        }

        input,
        textarea,
        div[data-baseweb="input"],
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"],
        div[data-baseweb="textarea"] textarea {
            background-color: #ffffff !important;
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
            border-color: #cfe8e5 !important;
        }

        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #111827 !important;
            border-color: #cfe8e5 !important;
        }

        div[data-baseweb="select"] span,
        div[data-baseweb="select"] input {
            color: #111827 !important;
            -webkit-text-fill-color: #111827 !important;
        }

        div[data-baseweb="popover"],
        div[data-baseweb="menu"] {
            background-color: #ffffff !important;
            color: #111827 !important;
        }

        ul[role="listbox"] li,
        div[role="option"] {
            color: #111827 !important;
            background-color: #ffffff !important;
        }

        ul[role="listbox"] li:hover,
        div[role="option"]:hover {
            background-color: #e6fffb !important;
        }

        /* =========================
           BOTONES Y TABLAS
        ========================== */
        .stButton > button {
            background: #006d77 !important;
            color: white !important;
            border: 0 !important;
            border-radius: 12px !important;
            font-weight: 750 !important;
            padding: .55rem 1rem !important;
        }

        .stButton > button:hover {
            background: #00515a !important;
            color: white !important;
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid #d9ecea;
            box-shadow: 0 8px 20px rgba(15, 76, 83, .04);
        }

        hr {
            border-color: #d9ecea !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


def header():
    st.markdown(
        """
        <div class="portal-header">
            <h1>VitalCare Centro de Salud</h1>
            <p>
                Portal administrativo para gestionar pacientes, diagnósticos, horarios y vacaciones,
                con acceso a los reportes principales del centro de salud.
            </p>
            <span class="badge">MySQL conectado</span>
            <span class="badge">Gestión clínica</span>
            <span class="badge">Reportes operativos</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def title(text, subtitle):
    st.markdown(f"<div class='section-title'>{text}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='section-subtitle'>{subtitle}</div>", unsafe_allow_html=True)


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
    if df.empty:
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


apply_styles()

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <h2>🏥 VitalCare</h2>
            <p>Portal administrativo</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    try:
        if test_connection():
            st.success("Base de datos conectada")
    except Exception as e:
        st.error("No fue posible conectar con MySQL.")
        st.exception(e)
        st.stop()

    page = st.radio(
        "Menú principal",
        [
            "Inicio",
            "Gestión clínica",
            "Gestión médica",
            "Reportes del centro",
        ]
    )

    st.divider()
    st.caption("Bases de Datos Avanzadas")


header()


if page == "Inicio":
    title("Panel general", "Vista rápida del estado operativo y clínico del centro de salud.")

    try:
        data = resumen_dashboard().iloc[0]

        c1, c2, c3 = st.columns(3)
        with c1:
            metric_card("Pacientes", int(data["total_pacientes"]), "Pacientes registrados")
        with c2:
            metric_card("Médicos", int(data["total_medicos"]), "Personal médico registrado")
        with c3:
            metric_card("Diagnósticos", int(data["total_diagnosticos"]), "Registros clínicos")

        c4, c5, c6 = st.columns(3)
        with c4:
            metric_card("Empleados", int(data["total_empleados"]), "Médicos y personal general")
        with c5:
            metric_card("Horarios", int(data["total_horarios"]), "Franjas de consulta")
        with c6:
            metric_card("Vacaciones", int(data["vacaciones_planeadas"]), "Periodos planeados")
    except Exception as e:
        st.error("No se pudo cargar el panel general.")
        st.exception(e)

    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        module_card("Gestión clínica", "Consulta y administración básica de pacientes y diagnósticos.")
    with c2:
        module_card("Gestión médica", "Directorio de médicos, horarios de consulta y vacaciones.")
    with c3:
        module_card("Reportes del centro", "Consultas oficiales solicitadas en el enunciado del proyecto.")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
        st.subheader("Agenda de hoy")
        show_table(agenda_hoy(), "No hay consultas programadas para hoy.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='soft-panel'>", unsafe_allow_html=True)
        st.subheader("Últimos diagnósticos")
        show_table(ultimos_diagnosticos(6), "No hay diagnósticos registrados.")
        st.markdown("</div>", unsafe_allow_html=True)


elif page == "Gestión clínica":
    title("Gestión clínica", "Operaciones básicas sobre pacientes y diagnósticos.")

    seccion = st.selectbox(
        "Selecciona una sección",
        ["Pacientes", "Diagnósticos"],
        key="gestion_clinica_seccion"
    )

    if seccion == "Pacientes":
        st.markdown(
            "<div class='notice'>Aquí se pueden registrar, consultar, actualizar y eliminar pacientes.</div>",
            unsafe_allow_html=True
        )

        st.subheader("Consulta de pacientes")
        busqueda = st.text_input("Buscar paciente", placeholder="Nombre, médico, especialidad, municipio o ID")
        show_table(buscar_pacientes(busqueda.strip()), "No se encontraron pacientes.")

        st.divider()
        st.subheader("Operaciones")

        operacion = st.selectbox(
            "Operación sobre pacientes",
            ["Registrar paciente", "Actualizar paciente", "Eliminar paciente"]
        )

        if operacion == "Registrar paciente":
            with st.form("form_crear_paciente"):
                nombre = st.text_input("Nombre completo")
                direccion = st.text_input("Dirección")
                telefono = st.text_input("Teléfono principal opcional")
                id_municipio = pair_select("Municipio", opciones_municipios(), key="crear_paciente_municipio")
                id_medico = pair_select("Médico responsable", opciones_medicos(), key="crear_paciente_medico")
                enviar = st.form_submit_button("Guardar paciente")

                if enviar:
                    if not nombre.strip() or not direccion.strip() or id_municipio is None or id_medico is None:
                        st.warning("Completa nombre, dirección, municipio y médico.")
                    else:
                        try:
                            nuevo_id = crear_paciente(nombre.strip(), direccion.strip(), id_municipio, id_medico, telefono)
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
                            "Municipio",
                            municipios,
                            key="actualizar_paciente_municipio",
                            selected_id=int(actual["id_municipio"])
                        )
                        id_medico = pair_select(
                            "Médico responsable",
                            medicos,
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
            st.markdown(
                "<div class='danger'>Usa esta opción solo para pruebas. Al eliminar un paciente se eliminan también sus teléfonos y diagnósticos asociados.</div>",
                unsafe_allow_html=True
            )
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

    elif seccion == "Diagnósticos":
        st.subheader("Últimos diagnósticos")
        show_table(ultimos_diagnosticos(15), "No hay diagnósticos registrados.")

        st.divider()
        st.subheader("Operaciones")

        operacion = st.selectbox(
            "Operación sobre diagnósticos",
            ["Registrar diagnóstico", "Actualizar diagnóstico", "Eliminar diagnóstico"]
        )

        if operacion == "Registrar diagnóstico":
            with st.form("form_crear_diagnostico"):
                id_paciente = pair_select("Paciente", opciones_pacientes(), key="crear_diag_paciente")
                fecha_diag = st.date_input("Fecha", value=date.today())
                enfermedades = opciones_enfermedades()
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
                    diag_final = enfermedad_sel if enfermedad_sel else descripcion.strip() if descripcion else ""
                    if id_paciente is None or not diag_final:
                        st.warning("Selecciona un paciente y una enfermedad o escribe la descripción.")
                    else:
                        try:
                            nuevo_id = crear_diagnostico(id_paciente, fecha_diag, diag_final)
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


elif page == "Gestión médica":
    title("Gestión médica", "Consulta de médicos, agenda semanal, horarios y vacaciones.")

    seccion = st.selectbox(
        "Selecciona una sección",
        ["Directorio médico", "Horarios de consulta", "Vacaciones"],
        key="gestion_medica_seccion"
    )

    if seccion == "Directorio médico":
        st.subheader("Directorio médico")
        busqueda = st.text_input("Buscar médico", placeholder="Nombre, especialidad, tipo o licencia")
        show_table(directorio_medicos(busqueda.strip()), "No se encontraron médicos.")

    elif seccion == "Horarios de consulta":
        st.subheader("Horarios de consulta")

        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        vista = st.selectbox(
            "Vista de horarios",
            ["Agenda semanal completa", "Agenda por día", "Registrar horario", "Eliminar horario"]
        )

        if vista == "Agenda semanal completa":
            show_table(agenda_semanal(), "No hay horarios registrados.")

        elif vista == "Agenda por día":
            dia = st.selectbox("Día", dias)
            show_table(agenda_por_dia(dia), "No hay horarios para ese día.")

        elif vista == "Registrar horario":
            with st.form("form_crear_horario"):
                id_medico = pair_select("Médico", opciones_medicos(), key="crear_horario_medico")
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
                            st.success(f"Horario registrado correctamente. ID: {nuevo_id}")
                        except Exception as e:
                            st.error("No se pudo registrar el horario. Revisa si ya existe un horario igual.")
                            st.exception(e)

        elif vista == "Eliminar horario":
            show_table(agenda_semanal(), "No hay horarios registrados.")
            id_horario = pair_select("Horario a eliminar", opciones_horarios(), key="eliminar_horario_select")
            confirmar = st.checkbox("Confirmo que deseo eliminar este horario")

            if st.button("Eliminar horario"):
                if not confirmar:
                    st.warning("Marca la casilla de confirmación.")
                else:
                    try:
                        eliminar_horario(id_horario)
                        st.success("Horario eliminado correctamente.")
                    except Exception as e:
                        st.error("No se pudo eliminar el horario.")
                        st.exception(e)

    elif seccion == "Vacaciones":
        st.subheader("Vacaciones")

        vista = st.selectbox(
            "Vista de vacaciones",
            ["Listado general", "Registrar vacaciones", "Eliminar vacaciones"]
        )

        if vista == "Listado general":
            busqueda = st.text_input("Buscar por empleado o especialidad")
            show_table(listado_vacaciones(busqueda.strip()), "No hay vacaciones registradas.")

        elif vista == "Registrar vacaciones":
            with st.form("form_crear_vacacion"):
                id_empleado = pair_select("Empleado", opciones_empleados(), key="crear_vacacion_empleado")
                fecha_inicio = st.date_input("Fecha inicio", value=date.today())
                fecha_fin = st.date_input("Fecha fin", value=date.today())
                enviar = st.form_submit_button("Guardar vacaciones")

                if enviar:
                    if fecha_fin < fecha_inicio:
                        st.warning("La fecha final no puede ser menor que la fecha inicial.")
                    else:
                        try:
                            nuevo_id = crear_vacacion(id_empleado, fecha_inicio, fecha_fin)
                            st.success(f"Vacaciones registradas correctamente. ID: {nuevo_id}")
                        except Exception as e:
                            st.error("No se pudieron registrar las vacaciones.")
                            st.exception(e)

        elif vista == "Eliminar vacaciones":
            show_table(listado_vacaciones(), "No hay vacaciones registradas.")
            id_vacacion = pair_select("Periodo a eliminar", opciones_vacaciones(), key="eliminar_vacacion_select")
            confirmar = st.checkbox("Confirmo que deseo eliminar este periodo de vacaciones")

            if st.button("Eliminar vacaciones"):
                if not confirmar:
                    st.warning("Marca la casilla de confirmación.")
                else:
                    try:
                        eliminar_vacacion(id_vacacion)
                        st.success("Periodo de vacaciones eliminado correctamente.")
                    except Exception as e:
                        st.error("No se pudo eliminar el periodo.")
                        st.exception(e)


elif page == "Reportes del centro":
    title("Reportes del centro", "Consultas oficiales solicitadas en el enunciado.")

    st.markdown(
        "<div class='notice'>Esta sección agrupa los 4 reportes mínimos exigidos para la entrega y sustentación del proyecto.</div>",
        unsafe_allow_html=True
    )

    reporte = st.selectbox(
        "Seleccione el reporte",
        [
            "1. Pacientes por especialidad del médico",
            "2. Médicos disponibles por especialidad",
            "3. Pacientes por diagnóstico",
            "4. Vacaciones de médicos en intervalo",
        ]
    )

    if reporte == "1. Pacientes por especialidad del médico":
        st.subheader("Pacientes a cargo de médicos según especialidad")
        especialidad = st.selectbox("Especialidad", get_especialidades(), key="r1_especialidad")
        if st.button("Generar reporte"):
            show_table(pacientes_por_especialidad(especialidad), "No hay pacientes para esa especialidad.")

    elif reporte == "2. Médicos disponibles por especialidad":
        st.subheader("Médicos disponibles para una especialidad")
        especialidad = st.selectbox("Especialidad", get_especialidades(), key="r2_especialidad")
        if st.button("Generar reporte"):
            show_table(medicos_disponibles_por_especialidad(especialidad), "No hay médicos disponibles para esa especialidad.")

    elif reporte == "3. Pacientes por diagnóstico":
        st.subheader("Pacientes diagnosticados con determinada enfermedad")
        texto = st.text_input("Enfermedad o palabra clave", placeholder="Ejemplo: Hipertensión, Diabetes, Asma")
        if st.button("Generar reporte"):
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

        if st.button("Generar reporte"):
            if fecha_fin < fecha_inicio:
                st.warning("La fecha final no puede ser menor que la inicial.")
            else:
                show_table(vacaciones_medicos_intervalo(fecha_inicio, fecha_fin), "No hay médicos con vacaciones en ese intervalo.")
