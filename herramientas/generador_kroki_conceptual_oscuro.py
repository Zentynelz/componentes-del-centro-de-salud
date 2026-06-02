import urllib.request
import os

dot_payload = """
graph G {
    bgcolor="#18181A"; 
    nodesep=0.5;
    ranksep=0.8;
    layout=dot;
    splines=ortho;
    
    node [fontname="Helvetica", fontcolor=white, color=white, shape=ellipse, style=solid, penwidth=1];
    edge [fontname="Helvetica", fontcolor=white, color=white, penwidth=1];

    // Entidades
    node [shape=box];
    MEDICO;
    EMPLEADO;
    PACIENTE;
    VACACIONES [peripheries=2];
    HORARIO [peripheries=2];
    PERIODO_SUSTITUTO [peripheries=2];
    DIAGNOSTICO [peripheries=2];
    ENFERMEDAD;
    USUARIO;
    
    // Relaciones (rombos normales)
    node [shape=diamond];
    DISFRUTAR;
    ATENDER;
    TENER;
    REALIZAR;
    HACER;
    CREA_PACIENTE;
    CREA_DIAGNOSTICO;
    IDENTIFICA;
    
    // Herencia / Generalización
    // Triángulo con vértice hacia EMPLEADO (superclase) y base hacia MEDICO (subclase)
    node [shape=triangle, label="ISA"];
    ISA;
    
    // Reset para los Atributos (elipses)
    node [shape=ellipse, label=""];
    
    // Atributos de MEDICO
    m_num [label=<<U>num_licencia</U>>];
    m_esp [label="especialidad"];
    m_tip [label="tipo_vinculacion"];
    
    MEDICO -- m_num; 
    MEDICO -- m_esp; 
    MEDICO -- m_tip; 
    
    // Atributos de EMPLEADO
    e_id [label=<<U>id_empleado</U>>];
    e_pro [label="profesion"];
    e_nom [label="nombre"];
    e_dir [label="direccion"];
    e_mun [label="municipio"];
    node [peripheries=2]; e_tel [label="telefonos"]; node [peripheries=1];
    
    EMPLEADO -- e_id; EMPLEADO -- e_pro; EMPLEADO -- e_nom;
    EMPLEADO -- e_dir; EMPLEADO -- e_mun; EMPLEADO -- e_tel;
    
    // Atributos de PACIENTE
    p_id [label=<<U>id_paciente</U>>];
    p_nom [label="nombre"];
    p_dir [label="direccion"];
    p_mun [label="municipio"];
    p_crea [label="id_usuario_creacion"];
    node [peripheries=2]; p_tel [label="telefonos"]; node [peripheries=1];
    
    PACIENTE -- p_id; PACIENTE -- p_nom; PACIENTE -- p_dir;
    PACIENTE -- p_mun; PACIENTE -- p_crea; PACIENTE -- p_tel;
    
    // Atributos de VACACIONES
    v_id [label=<<U>id_vacacion</U>>]; 
    v_ini [label="fecha_inicio"];
    v_fin [label="fecha_fin"];
    // El estado se calcula dinamicamente (no se almacena como atributo)
    
    VACACIONES -- v_id; 
    VACACIONES -- v_ini; VACACIONES -- v_fin;
    
    // Atributos de HORARIO
    h_tur [label=<<U>id_horario</U>>];
    h_dia [label="dia_semana"];
    h_ini [label="hora_inicio"];
    h_fin [label="hora_fin"];
    
    HORARIO -- h_tur; HORARIO -- h_dia; HORARIO -- h_ini; HORARIO -- h_fin;
    
    // Atributos de PERIODO_SUSTITUTO
    s_con [label=<<U>id_periodo</U>>];
    s_ing [label="fecha_ingreso"];
    s_ret [label="fecha_retiro"];
    
    PERIODO_SUSTITUTO -- s_con; PERIODO_SUSTITUTO -- s_ing; PERIODO_SUSTITUTO -- s_ret;
    
    // Atributos de DIAGNOSTICO
    d_num [label=<<U>id_diagnostico</U>>];
    d_fec [label="fecha"];
    d_des [label="descripcion"];
    d_crea [label="id_usuario_creacion"];
    
    DIAGNOSTICO -- d_num; DIAGNOSTICO -- d_fec; DIAGNOSTICO -- d_des;
    DIAGNOSTICO -- d_crea;
    
    // Atributos de ENFERMEDAD
    enf_id [label=<<U>id_enfermedad</U>>];
    enf_nom [label="nombre"];
    
    ENFERMEDAD -- enf_id; ENFERMEDAD -- enf_nom;
    
    // Atributos de USUARIO
    u_id [label=<<U>id_usuario</U>>];
    u_user [label="username"];
    u_pass [label="password_hash"];
    u_nom [label="nombre_completo"];
    u_rol [label="rol"];
    u_act [label="activo"];
    u_fec [label="fecha_creacion"];
    
    USUARIO -- u_id; USUARIO -- u_user; USUARIO -- u_pass;
    USUARIO -- u_nom; USUARIO -- u_rol; USUARIO -- u_act;
    USUARIO -- u_fec;
    
    // CONEXIONES DE RELACIONES Y ENTIDADES
    
    EMPLEADO -- ISA [dir=back];
    ISA -- MEDICO;

    EMPLEADO -- DISFRUTAR;
    DISFRUTAR -- VACACIONES;
    
    MEDICO -- TENER;
    TENER -- HORARIO;
    
    MEDICO -- REALIZAR;
    REALIZAR -- PERIODO_SUSTITUTO;
    
    MEDICO -- ATENDER;
    ATENDER -- PACIENTE;
    
    PACIENTE -- HACER;
    HACER -- DIAGNOSTICO;
    
    USUARIO -- CREA_PACIENTE;
    CREA_PACIENTE -- PACIENTE;
    
    USUARIO -- CREA_DIAGNOSTICO;
    CREA_DIAGNOSTICO -- DIAGNOSTICO;
    
    DIAGNOSTICO -- IDENTIFICA;
    IDENTIFICA -- ENFERMEDAD;
}
"""

try:
    headers = {
        "Content-Type": "text/plain",
        "User-Agent": "Mozilla/5.0"
    }
    req = urllib.request.Request("https://kroki.io/graphviz/png", data=dot_payload.encode('utf-8'), headers=headers)
    response = urllib.request.urlopen(req)
    png_data = response.read()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "..", "Diagrama_ER_Oscuro_Normalizado.png")
    
    with open(output_path, "wb") as f:
        f.write(png_data)
    print(f"Éxito! Archivo generado distribuido en negro: {output_path}")

except Exception as e:
    print("Fallo critico al generar:", e)
