# -*- coding: utf-8 -*-
"""
auth.py - Módulo de autenticación para VitalCare Centro de Salud
Maneja login, logout, verificación de sesión y roles.
"""

import hashlib
import streamlit as st
from db import fetch_dataframe, execute_query


def hash_password(password: str) -> str:
    """Retorna SHA-256 del password."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def autenticar(username: str, password: str) -> dict | None:
    """
    Verifica username/password contra la BD.
    Retorna dict con datos del usuario o None si falla.
    """
    df = fetch_dataframe(
        "SELECT id_usuario, username, nombre_completo, rol "
        "FROM vw_usuarios_activos WHERE username = %s",
        (username,)
    )
    if df.empty:
        return None

    # Verificar password
    df_pw = fetch_dataframe(
        "SELECT password_hash FROM usuario WHERE id_usuario = %s",
        (int(df.iloc[0]["id_usuario"]),)
    )
    if df_pw.empty:
        return None

    if df_pw.iloc[0]["password_hash"] != hash_password(password):
        return None

    return {
        "id_usuario": int(df.iloc[0]["id_usuario"]),
        "username": str(df.iloc[0]["username"]),
        "nombre_completo": str(df.iloc[0]["nombre_completo"]),
        "rol": str(df.iloc[0]["rol"]),
    }


def iniciar_sesion(usuario: dict):
    """Guarda el usuario en la sesión de Streamlit."""
    st.session_state["usuario"] = usuario
    st.session_state["logueado"] = True


def cerrar_sesion():
    """Limpia la sesión."""
    for key in ["usuario", "logueado"]:
        if key in st.session_state:
            del st.session_state[key]


def sesion_activa() -> bool:
    """Retorna True si hay un usuario logueado."""
    return st.session_state.get("logueado", False)


def usuario_actual() -> dict | None:
    """Retorna el usuario logueado o None."""
    return st.session_state.get("usuario", None)


def tiene_rol(*roles: str) -> bool:
    """Verifica si el usuario actual tiene alguno de los roles dados."""
    usuario = usuario_actual()
    if not usuario:
        return False
    return usuario["rol"] in roles


def es_admin() -> bool:
    """Verifica si el usuario actual es admin."""
    return tiene_rol("admin")


def login_required():
    """
    Decorador/Mostrador de pantalla de login.
    Si no hay sesión activa, muestra el formulario de login y detiene.
    """
    if not sesion_activa():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown(
                """
                <div style="text-align: center; padding: 2rem 0;">
                    <h1 style="color: #f5c842;">🏥 VitalCare</h1>
                    <p style="color: #b0b0b0; font-size: 1.1rem;">
                        Centro de Salud — Sistema de Gestión
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.container():
                st.markdown("### Inicio de sesión")
                username = st.text_input("Usuario", placeholder="Ej: admin")
                password = st.text_input(
                    "Contraseña",
                    type="password",
                    placeholder="••••••••",
                )
                if st.button("Ingresar", use_container_width=True, type="primary"):
                    if not username or not password:
                        st.error("Ingresa usuario y contraseña.")
                    else:
                        usuario = autenticar(username, password)
                        if usuario:
                            iniciar_sesion(usuario)
                            st.rerun()
                        else:
                            st.error("Usuario o contraseña incorrectos.")
            st.markdown(
                """
                <div style="text-align: center; padding: 1rem 0;">
                    <p style="color: #666; font-size: 0.8rem;">
                        Usuarios por defecto: admin / dr.garcia / enfermera.lopez / recepcion<br>
                        Contraseña: admin123
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
        return False
    return True


def mostrar_info_usuario():
    """Muestra la info del usuario con botón de salir."""
    usuario = usuario_actual()
    if usuario:
        roles_emoji = {
            "admin": "🛡️",
            "medico": "👨‍⚕️",
            "enfermero": "👩‍⚕️",
            "recepcionista": "💁",
        }
        emoji = roles_emoji.get(usuario["rol"], "👤")
        # Mostrar usuario
        st.markdown(
            f"<div style='padding:4px 0;margin-bottom:6px;'>"
            f"<span style='color:#f5c842;font-size:0.9rem;font-weight:700;'>{emoji} {usuario['nombre_completo']}</span><br>"
            f"<span style='color:#8b949e;font-size:0.8rem;'>Rol: {usuario['rol'].capitalize()}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )
        # Botón de salir estilizado
        st.markdown("""
        <style>
        div[data-testid="stButton"] button[kind="secondary"] {
            background: transparent !important;
            border: 1px solid #e9456066 !important;
            color: #e94560 !important;
            border-radius: 8px !important;
            font-size: 0.8rem !important;
            padding: 4px 12px !important;
        }
        div[data-testid="stButton"] button[kind="secondary"]:hover {
            background: rgba(233, 69, 96, 0.1) !important;
            border-color: #e94560 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        if st.button("🚪 Salir", key="btn_logout", use_container_width=True, type="secondary"):
            cerrar_sesion()
            st.rerun()


def listar_usuarios() -> list[tuple]:
    """Retorna lista de (id_usuario, nombre_completo) para dropdowns."""
    from db import fetch_pairs
    return fetch_pairs(
        "SELECT id_usuario, CONCAT(nombre_completo, ' (', rol, ')') "
        "FROM usuario WHERE activo = TRUE ORDER BY nombre_completo"
    )


def crear_usuario(username: str, password: str, nombre_completo: str, rol: str) -> int:
    """Crea un nuevo usuario. Retorna el id."""
    pw_hash = hash_password(password)
    return execute_query(
        "INSERT INTO usuario (username, password_hash, nombre_completo, rol) VALUES (%s, %s, %s, %s)",
        (username, pw_hash, nombre_completo, rol),
    )


def actualizar_usuario(id_usuario: int, nombre_completo: str, rol: str, activo: bool):
    """Actualiza datos de un usuario."""
    execute_query(
        "UPDATE usuario SET nombre_completo = %s, rol = %s, activo = %s WHERE id_usuario = %s",
        (nombre_completo, rol, activo, id_usuario),
    )


def cambiar_password(id_usuario: int, nuevo_password: str):
    """Cambia la contraseña de un usuario."""
    pw_hash = hash_password(nuevo_password)
    execute_query(
        "UPDATE usuario SET password_hash = %s WHERE id_usuario = %s",
        (pw_hash, id_usuario),
    )
