-- ==========================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Gestión de Prácticas - MySQL 8.x
-- ==========================================================

DROP DATABASE IF EXISTS gestion_practicas;

-- Crear la base de datos (si no existe)
CREATE DATABASE IF NOT EXISTS gestion_practicas
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE gestion_practicas;

-- ==========================================================
-- Eliminación de tablas (en orden inverso a las dependencias)
-- ==========================================================
DROP TABLE IF EXISTS LOGS_SISTEMA;
DROP TABLE IF EXISTS INDICADORES_ANALITICOS;
DROP TABLE IF EXISTS DOCUMENTOS;
DROP TABLE IF EXISTS INCIDENCIAS;
DROP TABLE IF EXISTS EVALUACIONES;
DROP TABLE IF EXISTS REGISTROS_ACTIVIDAD;
DROP TABLE IF EXISTS PRACTICAS;
DROP TABLE IF EXISTS CONVENIOS;
DROP TABLE IF EXISTS EMPRESAS;
DROP TABLE IF EXISTS TUTORES;
DROP TABLE IF EXISTS ESTUDIANTES;
DROP TABLE IF EXISTS CENTROS_EDUCATIVOS;

-- ==========================================================
-- CREACIÓN DE TABLAS
-- ==========================================================

CREATE TABLE CENTROS_EDUCATIVOS (
    id_centro INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    direccion VARCHAR(255),
    provincia VARCHAR(100),
    tipo_centro VARCHAR(100)
);

CREATE TABLE ESTUDIANTES (
    id_estudiante INT AUTO_INCREMENT PRIMARY KEY,
    dni VARCHAR(15) UNIQUE NOT NULL,
    nombre VARCHAR(150) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(20),
    nacionalidad VARCHAR(50),
    id_centro INT NOT NULL,
    titulacion VARCHAR(150),
    curso_academico VARCHAR(20),
    FOREIGN KEY (id_centro) REFERENCES CENTROS_EDUCATIVOS(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE TUTORES (
    id_tutor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(20),
    id_centro INT NOT NULL,
    especialidad VARCHAR(150),
    FOREIGN KEY (id_centro) REFERENCES CENTROS_EDUCATIVOS(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE EMPRESAS (
    id_empresa INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    sector VARCHAR(100),
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    persona_contacto VARCHAR(150),
    correo_contacto VARCHAR(150),
    telefono_contacto VARCHAR(20),
    satisfaccion_media DECIMAL(4,2)
);

CREATE TABLE CONVENIOS (
    id_convenio INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    id_centro INT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    observaciones TEXT,
    FOREIGN KEY (id_empresa) REFERENCES EMPRESAS(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_centro) REFERENCES CENTROS_EDUCATIVOS(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE PRACTICAS (
    id_practica INT AUTO_INCREMENT PRIMARY KEY,
    id_estudiante INT NOT NULL,
    id_tutor INT NOT NULL,
    id_empresa INT NOT NULL,
    id_convenio INT NOT NULL,
    fecha_inicio DATE,
    fecha_fin DATE,
    horas_totales INT,
    estado ENUM('pendiente', 'en curso', 'finalizada', 'cancelada') DEFAULT 'pendiente',
    evaluacion_final DECIMAL(4,2),
    FOREIGN KEY (id_estudiante) REFERENCES ESTUDIANTES(id_estudiante)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_tutor) REFERENCES TUTORES(id_tutor)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_empresa) REFERENCES EMPRESAS(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_convenio) REFERENCES CONVENIOS(id_convenio)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE REGISTROS_ACTIVIDAD (
    id_registro INT AUTO_INCREMENT PRIMARY KEY,
    id_practica INT NOT NULL,
    fecha DATE,
    descripcion TEXT,
    -- CAMBIAR HORAS POR TIEMPO_DEDICADO
    horas INT,
    validado_por_tutor BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_practica) REFERENCES PRACTICAS(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE EVALUACIONES (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    id_practica INT NOT NULL,
    tipo ENUM('inicial', 'intermedia', 'final'),
    fecha DATE,
    puntuacion DECIMAL(4,2),
    comentarios TEXT,
    FOREIGN KEY (id_practica) REFERENCES PRACTICAS(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE INCIDENCIAS (
    id_incidencia INT AUTO_INCREMENT PRIMARY KEY,
    id_practica INT NOT NULL,
    fecha DATE,
    descripcion TEXT,
    tipo ENUM('leve', 'moderada', 'grave'),
    resuelta BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_practica) REFERENCES PRACTICAS(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE DOCUMENTOS (
    id_documento INT AUTO_INCREMENT PRIMARY KEY,
    id_practica INT NOT NULL,
    tipo ENUM('informe', 'evaluacion', 'anexo', 'otro'),
    nombre_archivo VARCHAR(255),
    ruta_archivo VARCHAR(255),
    fecha_subida DATETIME DEFAULT CURRENT_TIMESTAMP,
    tamano BIGINT,
    FOREIGN KEY (id_practica) REFERENCES PRACTICAS(id_practica)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE INDICADORES_ANALITICOS (
    id_indicador INT AUTO_INCREMENT PRIMARY KEY,
    id_empresa INT NOT NULL,
    id_centro INT NOT NULL,
    anio INT,
    practicas_realizadas INT,
    tasa_finalizacion DECIMAL(5,2),
    satisfaccion_media DECIMAL(4,2),
    tasa_contratacion DECIMAL(5,2),
    abandonos INT,
    FOREIGN KEY (id_empresa) REFERENCES EMPRESAS(id_empresa)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    FOREIGN KEY (id_centro) REFERENCES CENTROS_EDUCATIVOS(id_centro)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE LOGS_SISTEMA (
    id_log BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT,
    tipo_evento VARCHAR(100),
    fecha_evento DATETIME DEFAULT CURRENT_TIMESTAMP,
    detalle TEXT,
    ip VARCHAR(45)
);

-- ==========================================================
-- FIN DEL SCRIPT
-- ==========================================================
