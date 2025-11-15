-- ==========================================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Gestión de Prácticas - PostgreSQL 16+
-- ==========================================================

DROP DATABASE IF EXISTS gestion_practicas;

CREATE DATABASE gestion_practicas
    WITH 
    OWNER = root
    ENCODING = 'UTF8'
    LC_COLLATE = 'C'
    LC_CTYPE = 'C'
    TEMPLATE = template0
    CONNECTION LIMIT = -1;

-- ==========================================================
-- FIN DEL SCRIPT
-- ==========================================================
