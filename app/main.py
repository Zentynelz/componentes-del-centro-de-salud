import streamlit as st
from datetime import date
from db import fetch_options, test_connection
from reports import (
    pacientes_por_especialidad,
    medicos_disponibles_por_especialidad,
    pacientes_por_diagnostico,
    vacaciones_medicos_intervalo,
)


st.set_page_config(
    page_title="Centro de Salud",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Sistema de Reportes - Centro de Salud")
st.write(
    "Aplicación conectada a MySQL para consultar los reportes solicitados "
    "en el proyecto final de Bases de Datos Avanzadas."
)

with st.sidebar:
    st.header("Menú")

    try:
        if test_connection():
            st.success("Conexión a MySQL exitosa")
    except Exception as e:
        st.error("No fue posible conectar con la base de datos.")
        st.exception(e)
        st.stop()

    reporte = st.radio(
        "Seleccione un reporte",
        [
            "1. Pacientes por especialidad del médico",
            "2. Médicos disponibles por especialidad",
            "3. Pacientes por diagnóstico",
            "4. Vacaciones de médicos por intervalo",
        ]
    )


def mostrar_tabla(df):
    if df.empty:
        st.warning("No se encontraron resultados para los filtros seleccionados.")
    else:
        st.success(f"Se encontraron {len(df)} registro(s).")
        st.dataframe(df, use_container_width=True)


if reporte == "1. Pacientes por especialidad del médico":
    st.subheader("Reporte 1: Pacientes a cargo de un médico según especialidad")

    especialidades = fetch_options("SELECT nombre FROM especialidad ORDER BY nombre;")
    especialidad = st.selectbox("Especialidad", especialidades)

    if st.button("Consultar reporte 1"):
        df = pacientes_por_especialidad(especialidad)
        mostrar_tabla(df)

elif reporte == "2. Médicos disponibles por especialidad":
    st.subheader("Reporte 2: Médicos disponibles para una especialidad")

    st.info(
        "Se consideran disponibles los médicos de la especialidad seleccionada "
        "que no estén actualmente en vacaciones. Si el médico es sustituto, "
        "debe tener un periodo de sustitución activo."
    )

    especialidades = fetch_options("SELECT nombre FROM especialidad ORDER BY nombre;")
    especialidad = st.selectbox("Especialidad", especialidades)

    if st.button("Consultar reporte 2"):
        df = medicos_disponibles_por_especialidad(especialidad)
        mostrar_tabla(df)

elif reporte == "3. Pacientes por diagnóstico":
    st.subheader("Reporte 3: Pacientes diagnosticados con determinada enfermedad")

    texto = st.text_input(
        "Ingrese enfermedad o palabra clave del diagnóstico",
        placeholder="Ejemplo: Hipertensión, Diabetes, Asma"
    )

    if st.button("Consultar reporte 3"):
        if not texto.strip():
            st.warning("Ingrese una enfermedad o palabra clave.")
        else:
            df = pacientes_por_diagnostico(texto.strip())
            mostrar_tabla(df)

elif reporte == "4. Vacaciones de médicos por intervalo":
    st.subheader("Reporte 4: Médicos con vacaciones en un intervalo de tiempo")

    col1, col2 = st.columns(2)

    with col1:
        fecha_inicio = st.date_input("Fecha inicial", value=date(2025, 1, 1))

    with col2:
        fecha_fin = st.date_input("Fecha final", value=date(2025, 12, 31))

    if st.button("Consultar reporte 4"):
        if fecha_fin < fecha_inicio:
            st.error("La fecha final no puede ser menor que la fecha inicial.")
        else:
            df = vacaciones_medicos_intervalo(fecha_inicio, fecha_fin)
            mostrar_tabla(df)
