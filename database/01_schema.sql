DROP DATABASE IF EXISTS centro_salud;
CREATE DATABASE centro_salud
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE centro_salud;

CREATE TABLE municipio (
    id_municipio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE profesion (
    id_profesion INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE especialidad (
    id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE tipo_medico (
    id_tipo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE
) ENGINE=InnoDB;

CREATE TABLE empleado (
    id_empleado INT AUTO_INCREMENT PRIMARY KEY,
    id_municipio INT NOT NULL,
    id_profesion INT NULL,
    nombre VARCHAR(120) NOT NULL,
    direccion VARCHAR(160) NOT NULL,
    CONSTRAINT fk_empleado_municipio
        FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio),
    CONSTRAINT fk_empleado_profesion
        FOREIGN KEY (id_profesion) REFERENCES profesion(id_profesion)
) ENGINE=InnoDB;

CREATE TABLE medico (
    id_empleado INT PRIMARY KEY,
    num_licencia VARCHAR(50) NOT NULL UNIQUE,
    id_tipo INT NOT NULL,
    id_especialidad INT NOT NULL,
    CONSTRAINT fk_medico_empleado
        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        ON DELETE CASCADE,
    CONSTRAINT fk_medico_tipo
        FOREIGN KEY (id_tipo) REFERENCES tipo_medico(id_tipo),
    CONSTRAINT fk_medico_especialidad
        FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad)
) ENGINE=InnoDB;

CREATE TABLE telefono_empleado (
    id_empleado INT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_empleado, telefono),
    CONSTRAINT fk_tel_empleado
        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE horario (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado_medico INT NOT NULL,
    dia_semana ENUM('Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    CONSTRAINT fk_horario_medico
        FOREIGN KEY (id_empleado_medico) REFERENCES medico(id_empleado)
        ON DELETE CASCADE,
    CONSTRAINT chk_horario_horas
        CHECK (hora_fin > hora_inicio),
    CONSTRAINT uq_horario_medico_dia_hora
        UNIQUE (id_empleado_medico, dia_semana, hora_inicio, hora_fin)
) ENGINE=InnoDB;

CREATE TABLE periodo_sustituto (
    id_periodo INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado_medico INT NOT NULL,
    fecha_ingreso DATE NOT NULL,
    fecha_retiro DATE NULL,
    CONSTRAINT fk_periodo_sustituto_medico
        FOREIGN KEY (id_empleado_medico) REFERENCES medico(id_empleado)
        ON DELETE CASCADE,
    CONSTRAINT chk_periodo_fechas
        CHECK (fecha_retiro IS NULL OR fecha_retiro >= fecha_ingreso)
) ENGINE=InnoDB;

CREATE TABLE vacaciones (
    id_vacacion INT AUTO_INCREMENT PRIMARY KEY,
    id_empleado INT NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    CONSTRAINT fk_vacaciones_empleado
        FOREIGN KEY (id_empleado) REFERENCES empleado(id_empleado)
        ON DELETE CASCADE,
    CONSTRAINT chk_vacaciones_fechas
        CHECK (fecha_fin >= fecha_inicio)
) ENGINE=InnoDB;

CREATE TABLE paciente (
    id_paciente INT AUTO_INCREMENT PRIMARY KEY,
    id_municipio INT NOT NULL,
    id_empleado_medico INT NOT NULL,
    nombre VARCHAR(120) NOT NULL,
    direccion VARCHAR(160) NOT NULL,
    CONSTRAINT fk_paciente_municipio
        FOREIGN KEY (id_municipio) REFERENCES municipio(id_municipio),
    CONSTRAINT fk_paciente_medico
        FOREIGN KEY (id_empleado_medico) REFERENCES medico(id_empleado)
) ENGINE=InnoDB;

CREATE TABLE telefono_paciente (
    id_paciente INT NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_paciente, telefono),
    CONSTRAINT fk_tel_paciente
        FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente)
        ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE diagnostico (
    id_diagnostico INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente INT NOT NULL,
    fecha DATE NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    CONSTRAINT fk_diagnostico_paciente
        FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente)
        ON DELETE CASCADE
) ENGINE=InnoDB;
