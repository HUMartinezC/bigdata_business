-- ==========================================================
-- SCRIPT DE CREACIÓN DE TABLAS
-- Sistema de Gestión de Prácticas - PostgreSQL 16+
-- ==========================================================

-- ==========================================================
-- Eliminación de tablas (orden inverso de dependencias)
-- ==========================================================
DROP TABLE IF EXISTS logs_sistema CASCADE;
DROP TABLE IF EXISTS indicadores_analiticos CASCADE;
DROP TABLE IF EXISTS documentos CASCADE;
DROP TABLE IF EXISTS incidencias CASCADE;
DROP TABLE IF EXISTS evaluaciones CASCADE;
DROP TABLE IF EXISTS registros_actividad CASCADE;
DROP TABLE IF EXISTS practicas CASCADE;
DROP TABLE IF EXISTS convenios CASCADE;
DROP TABLE IF EXISTS empresas CASCADE;
DROP TABLE IF EXISTS tutores CASCADE;
DROP TABLE IF EXISTS estudiantes CASCADE;
DROP TABLE IF EXISTS centros_educativos CASCADE;

-- ==========================================================
-- CREACIÓN DE TABLAS
-- ==========================================================

CREATE TABLE centros_educativos (
    id_centro SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255),
    provincia VARCHAR(100),
    tipo_centro VARCHAR(100)
);

CREATE TABLE estudiantes (
    id_estudiante SERIAL PRIMARY KEY,
    dni VARCHAR(15) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(20),
    nacionalidad VARCHAR(50),
    id_centro INT NOT NULL REFERENCES centros_educativos(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    titulacion VARCHAR(150),
    curso_academico VARCHAR(20)
);

CREATE TABLE tutores (
    id_tutor SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150),
    id_centro INT NOT NULL REFERENCES centros_educativos(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    especialidad VARCHAR(150)
);

CREATE TABLE empresas (
    id_empresa SERIAL PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    sector VARCHAR(100),
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    persona_contacto VARCHAR(150),
    correo_contacto VARCHAR(150),
    telefono_contacto VARCHAR(20),
    satisfaccion_media NUMERIC(4,2)
);

CREATE TABLE convenios (
    id_convenio SERIAL PRIMARY KEY,
    id_empresa INT NOT NULL REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_centro INT NOT NULL REFERENCES centros_educativos(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha_inicio DATE,
    fecha_fin DATE,
    observaciones TEXT
);

CREATE TABLE practicas (
    id_practica SERIAL PRIMARY KEY,
    id_estudiante INT NOT NULL REFERENCES estudiantes(id_estudiante)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_tutor INT NULL REFERENCES tutores(id_tutor)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
    id_empresa INT NOT NULL REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_convenio INT NOT NULL REFERENCES convenios(id_convenio)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha_inicio DATE,
    fecha_fin DATE,
    horas_totales INT,
    estado VARCHAR(20) CHECK (estado IN ('pendiente','en curso','finalizada','cancelada')) DEFAULT 'pendiente',
    evaluacion_final NUMERIC(4,2)
);

CREATE TABLE registros_actividad (
    id_registro SERIAL PRIMARY KEY,
    id_practica INT NOT NULL REFERENCES practicas(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha DATE,
    descripcion TEXT,
    horas INT,
    validado_por_tutor BOOLEAN DEFAULT FALSE
);

CREATE TABLE evaluaciones (
    id_evaluacion SERIAL PRIMARY KEY,
    id_practica INT NOT NULL REFERENCES practicas(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    tipo VARCHAR(20) CHECK (tipo IN ('inicial','intermedia','final')),
    fecha DATE,
    puntuacion NUMERIC(4,2),
    comentarios TEXT
);

CREATE TABLE incidencias (
    id_incidencia SERIAL PRIMARY KEY,
    id_practica INT NOT NULL REFERENCES practicas(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    fecha DATE,
    descripcion TEXT,
    tipo VARCHAR(20) CHECK (tipo IN ('leve','moderada','grave')),
    resuelta BOOLEAN DEFAULT FALSE
);

CREATE TABLE documentos (
    id_documento SERIAL PRIMARY KEY,
    id_practica INT NOT NULL REFERENCES practicas(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    tipo VARCHAR(20) CHECK (tipo IN ('informe','evaluacion','anexo','otro')),
    nombre_archivo VARCHAR(255),
    ruta_archivo VARCHAR(255),
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tamano BIGINT
);

CREATE TABLE indicadores_analiticos (
    id_indicador SERIAL PRIMARY KEY,
    id_empresa INT NOT NULL REFERENCES empresas(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    id_centro INT NOT NULL REFERENCES centros_educativos(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    anio INT,
    practicas_realizadas INT,
    tasa_finalizacion NUMERIC(5,2),
    satisfaccion_media NUMERIC(4,2),
    tasa_contratacion NUMERIC(5,2),
    abandonos INT
);

CREATE TABLE logs_sistema (
    id_log BIGSERIAL PRIMARY KEY,
    id_usuario INT,
    tipo_evento VARCHAR(100),
    fecha_evento TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalle TEXT,
    ip VARCHAR(45)
);

-- ==========================================================
-- FIN DEL SCRIPT
-- ==========================================================
