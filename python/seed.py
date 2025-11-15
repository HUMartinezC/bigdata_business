"""
Script para poblar las bases de datos MySQL con datos aleatorios usando Faker.
Se usan los siguientes 10 providers de Faker:

1. name
2. address
3. phone_number
4. email
5. date_of_birth
6. company
7. company_email
8. text
9. country
10. date_between
"""

import random
from datetime import timedelta
from faker import Faker

import oracledb
import psycopg2
import mysql.connector

# Cargamos la variables de entorno

fake = Faker('es_ES')

# Obtenemos las variables de entorno para activar las bases de datos

def ejecutar_bloque(db_name, cursor, commit_fn, rollback_fn, close_fn):
    """Ejecuta un bloque de inserciones en una base de datos específica."""

    # Logs iniciales

    print(f"\n{'='*60}")
    print(f"INICIANDO POBLACIÓN: {db_name.upper()}")
    print(f"{'='*60}\n")

    # Se insertan datos con Faker en todas las tablas
    
    def insertar_centros_educativos(n=10):
        print(f"Insertando {n} centros educativos...")
        for _ in range(n):
            nombre = f"Centro Educativo {fake.company()}"
            direccion = fake.address()
            provincia = fake.city()
            tipo_centro = random.choice(['Universidad', 'Instituto', 'Centro de Formación Profesional', 'Escuela Técnica'])
            
            # Condicional necesario para evitar errores de sintaxis en Oracle
            
            if db_name == "oracle":
                cursor.execute("INSERT INTO CENTROS_EDUCATIVOS (nombre, direccion, provincia, tipo_centro) VALUES (:1, :2, :3, :4)", (nombre, direccion, provincia, tipo_centro))
            else:
                cursor.execute("INSERT INTO CENTROS_EDUCATIVOS (nombre, direccion, provincia, tipo_centro) VALUES (%s, %s, %s, %s)", (nombre, direccion, provincia, tipo_centro))
        commit_fn()
        print(f"{n} centros educativos insertados")

    def insertar_empresas(n=15):
        print(f"Insertando {n} empresas...")
        for _ in range(n):
            nombre = fake.company()
            sector = random.choice(['Tecnología', 'Consultoría', 'Construcción', 'Educación', 'Sanidad', 'Comercio', 'Hostelería', 'Industria', 'Servicios'])
            direccion = fake.address()
            ciudad = fake.city()
            persona_contacto = fake.name()
            correo_contacto = fake.company_email()
            telefono = fake.phone_number()
            satisfaccion_media = round(random.uniform(6.0, 10.0), 2)
            if db_name == "oracle":
                cursor.execute("INSERT INTO EMPRESAS (nombre, sector, direccion, ciudad, persona_contacto, correo_contacto, telefono, satisfaccion_media) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", (nombre, sector, direccion, ciudad, persona_contacto, correo_contacto, telefono, satisfaccion_media))
            else:
                cursor.execute("INSERT INTO EMPRESAS (nombre, sector, direccion, ciudad, persona_contacto, correo_contacto, telefono, satisfaccion_media) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (nombre, sector, direccion, ciudad, persona_contacto, correo_contacto, telefono, satisfaccion_media))
        commit_fn()
        print(f"{n} empresas insertadas")

    def insertar_estudiantes(n=30):
        print(f"Insertando {n} estudiantes...")
        
        # Obtenemos los IDs necesarios para las relaciones necesarias
        
        cursor.execute("SELECT id_centro FROM CENTROS_EDUCATIVOS")
        centros_ids = [row[0] for row in cursor.fetchall()]
        for _ in range(n):
            dni = fake.unique.bothify(text='########?').upper()
            nombre = fake.name()
            fecha_nacimiento = fake.date_between(start_date='-30y', end_date='-18y')
            correo = fake.email()
            telefono = fake.phone_number()
            nacionalidad = fake.country()
            id_centro = random.choice(centros_ids) if centros_ids else None
            titulacion = random.choice(['Ingeniería Informática', 'Administración de Sistemas', 'Desarrollo de Aplicaciones Web', 'Desarrollo de Aplicaciones Multiplataforma', 'Ingeniería Industrial', 'Administración y Finanzas'])
            curso_academico = random.choice(['2023/2024', '2024/2025'])
            if db_name == "oracle":
                cursor.execute("INSERT INTO ESTUDIANTES (dni, nombre, fecha_nacimiento, correo, telefono, nacionalidad, id_centro, titulacion, curso_academico) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", (dni, nombre, fecha_nacimiento, correo, telefono, nacionalidad, id_centro, titulacion, curso_academico))
            else:
                cursor.execute("INSERT INTO ESTUDIANTES (dni, nombre, fecha_nacimiento, correo, telefono, nacionalidad, id_centro, titulacion, curso_academico) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (dni, nombre, fecha_nacimiento, correo, telefono, nacionalidad, id_centro, titulacion, curso_academico))
        commit_fn()
        print(f"{n} estudiantes insertados")

    def insertar_tutores(n=15):
        print(f"Insertando {n} tutores...")
        cursor.execute("SELECT id_centro FROM CENTROS_EDUCATIVOS")
        centros_ids = [row[0] for row in cursor.fetchall()]
        for _ in range(n):
            nombre = fake.name()
            correo = fake.email()
            id_centro = random.choice(centros_ids) if centros_ids else None
            especialidad = random.choice(['Programación', 'Bases de Datos', 'Redes', 'Ciberseguridad', 'Desarrollo Web', 'Sistemas Operativos', 'Administración de Sistemas'])
            if db_name == "oracle":
                cursor.execute("INSERT INTO TUTORES (nombre, correo, id_centro, especialidad) VALUES (:1, :2, :3, :4)", (nombre, correo, id_centro, especialidad))
            else:
                cursor.execute("INSERT INTO TUTORES (nombre, correo, id_centro, especialidad) VALUES (%s, %s, %s, %s)", (nombre, correo, id_centro, especialidad))
        commit_fn()
        print(f"{n} tutores insertados")

    def insertar_convenios(n=20):
        print(f"Insertando {n} convenios...")
        cursor.execute("SELECT id_empresa FROM EMPRESAS"); empresas_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id_centro FROM CENTROS_EDUCATIVOS"); centros_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_empresa = random.choice(empresas_ids)
            id_centro = random.choice(centros_ids)
            fecha_inicio = fake.date_between(start_date="-2y", end_date="-1y")
            fecha_fin = fecha_inicio + timedelta(days=random.randint(365, 1095))
            observaciones = fake.text(max_nb_chars=200)
            if db_name == "oracle":
                cursor.execute("INSERT INTO CONVENIOS (id_empresa, id_centro, fecha_inicio, fecha_fin, observaciones) VALUES (:1, :2, :3, :4, :5)", (id_empresa, id_centro, fecha_inicio, fecha_fin, observaciones))
            else:
                cursor.execute("INSERT INTO CONVENIOS (id_empresa, id_centro, fecha_inicio, fecha_fin, observaciones) VALUES (%s, %s, %s, %s, %s)", (id_empresa, id_centro, fecha_inicio, fecha_fin, observaciones))
        commit_fn()
        print(f"{n} convenios insertados")

    def insertar_practicas(n=40):
        print(f"Insertando {n} prácticas...")
        cursor.execute("SELECT id_estudiante FROM ESTUDIANTES"); estudiantes_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id_tutor FROM TUTORES"); tutores_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id_empresa FROM EMPRESAS"); empresas_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id_convenio FROM CONVENIOS"); convenios_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_estudiante = random.choice(estudiantes_ids)
            id_empresa = random.choice(empresas_ids)
            id_convenio = random.choice(convenios_ids)
            fecha_inicio = fake.date_between(start_date="-1y", end_date="-3m")
            fecha_fin = fecha_inicio + timedelta(days=random.randint(60, 180))
            horas_totales = random.randint(200, 600)
            estado = random.choice(['pendiente', 'en curso', 'finalizada', 'cancelada'])
            evaluacion_final = round(random.uniform(5.0, 10.0), 2) if estado == 'finalizada' else None

            # id_tutor: Oracle permite NULL, PG/MySQL NO
            if db_name == "oracle":
                id_tutor = random.choice(tutores_ids) if random.random() > 0.1 else None
            else:
                id_tutor = random.choice(tutores_ids)  # Siempre valor

            if db_name == "oracle":
                cursor.execute("INSERT INTO PRACTICAS (id_estudiante, id_tutor, id_empresa, id_convenio, fecha_inicio, fecha_fin, horas_totales, estado, evaluacion_final) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)", (id_estudiante, id_tutor, id_empresa, id_convenio, fecha_inicio, fecha_fin, horas_totales, estado, evaluacion_final))
            else:
                cursor.execute("INSERT INTO PRACTICAS (id_estudiante, id_tutor, id_empresa, id_convenio, fecha_inicio, fecha_fin, horas_totales, estado, evaluacion_final) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (id_estudiante, id_tutor, id_empresa, id_convenio, fecha_inicio, fecha_fin, horas_totales, estado, evaluacion_final))
        commit_fn()
        print(f"{n} prácticas insertadas")

    def insertar_registros_actividad(n=100):
        print(f"Insertando {n} registros de actividad...")
        cursor.execute("SELECT id_practica FROM PRACTICAS"); practicas_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_practica = random.choice(practicas_ids)
            fecha = fake.date_between(start_date="-6m", end_date="today")
            descripcion = fake.text(max_nb_chars=300)
            horas = random.randint(1, 8)
            validado = fake.boolean(chance_of_getting_true=75)
            if db_name == "oracle":
                cursor.execute("INSERT INTO REGISTROS_ACTIVIDAD (id_practica, fecha, descripcion, horas, validado_por_tutor) VALUES (:1, :2, :3, :4, :5)", (id_practica, fecha, descripcion, horas, '1' if validado else '0'))
            else:
                cursor.execute("INSERT INTO REGISTROS_ACTIVIDAD (id_practica, fecha, descripcion, horas, validado_por_tutor) VALUES (%s, %s, %s, %s, %s)", (id_practica, fecha, descripcion, horas, validado))
        commit_fn()
        print(f"{n} registros de actividad insertados")

    def insertar_evaluaciones(n=50):
        print(f"Insertando {n} evaluaciones...")
        cursor.execute("SELECT id_practica FROM PRACTICAS"); practicas_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_practica = random.choice(practicas_ids)
            tipo = random.choice(['intermedia', 'final'])
            fecha = fake.date_between(start_date="-6m", end_date="today")
            puntuacion = round(random.uniform(5.0, 10.0), 2)
            comentarios = fake.text(max_nb_chars=250)
            if db_name == "oracle":
                cursor.execute("INSERT INTO EVALUACIONES (id_practica, tipo, fecha, puntuacion, comentarios) VALUES (:1, :2, :3, :4, :5)", (id_practica, tipo, fecha, puntuacion, comentarios))
            else:
                cursor.execute("INSERT INTO EVALUACIONES (id_practica, tipo, fecha, puntuacion, comentarios) VALUES (%s, %s, %s, %s, %s)", (id_practica, tipo, fecha, puntuacion, comentarios))
        commit_fn()
        print(f"{n} evaluaciones insertadas")

    def insertar_incidencias(n=25):
        print(f"Insertando {n} incidencias...")
        cursor.execute("SELECT id_practica FROM PRACTICAS"); practicas_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_practica = random.choice(practicas_ids)
            fecha = fake.date_between(start_date="-6m", end_date="today")
            descripcion = fake.text(max_nb_chars=300)
            tipo = random.choice(['leve', 'moderada', 'grave'])
            resuelta = fake.boolean(chance_of_getting_true=70)
            if db_name == "oracle":
                cursor.execute("INSERT INTO INCIDENCIAS (id_practica, fecha, descripcion, tipo, resuelta) VALUES (:1, :2, :3, :4, :5)", (id_practica, fecha, descripcion, tipo, '1' if resuelta else '0'))
            else:
                cursor.execute("INSERT INTO INCIDENCIAS (id_practica, fecha, descripcion, tipo, resuelta) VALUES (%s, %s, %s, %s, %s)", (id_practica, fecha, descripcion, tipo, resuelta))
        commit_fn()
        print(f"{n} incidencias insertadas")

    def insertar_documentos(n=60):
        print(f"Insertando {n} documentos...")
        cursor.execute("SELECT id_practica FROM PRACTICAS"); practicas_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            id_practica = random.choice(practicas_ids)
            tipo = random.choice(['informe', 'anexo', 'evaluacion', 'otro'])
            nombre_archivo = fake.file_name(extension=random.choice(['pdf', 'docx', 'xlsx', 'zip']))
            ruta_archivo = f"/documentos/{id_practica}/{nombre_archivo}"
            tamano = random.randint(10240, 10485760)
            if db_name == "oracle":
                cursor.execute("INSERT INTO DOCUMENTOS (id_practica, tipo, nombre_archivo, ruta_archivo, tamano) VALUES (:1, :2, :3, :4, :5)", (id_practica, tipo, nombre_archivo, ruta_archivo, tamano))
            else:
                cursor.execute("INSERT INTO DOCUMENTOS (id_practica, tipo, nombre_archivo, ruta_archivo, tamano) VALUES (%s, %s, %s, %s, %s)", (id_practica, tipo, nombre_archivo, ruta_archivo, tamano))
        commit_fn()
        print(f"{n} documentos insertados")

    def insertar_indicadores_analiticos(n=30):
        print(f"Insertando {n} indicadores analíticos...")
        cursor.execute("SELECT id_empresa FROM EMPRESAS"); empresas_ids = [r[0] for r in cursor.fetchall()]
        cursor.execute("SELECT id_centro FROM CENTROS_EDUCATIVOS"); centros_ids = [r[0] for r in cursor.fetchall()]
        for _ in range(n):
            if db_name == "oracle":
                id_empresa = random.choice(empresas_ids) if random.random() > 0.3 else None
                id_centro = random.choice(centros_ids) if random.random() > 0.3 else None
            else:
                id_empresa = random.choice(empresas_ids)
                id_centro = random.choice(centros_ids)
            anio = random.choice([2021, 2022, 2023, 2024, 2025])
            practicas_realizadas = random.randint(5, 50)
            tasa_finalizacion = round(random.uniform(70.0, 98.0), 2)
            satisfaccion_media = round(random.uniform(6.0, 9.5), 2)
            tasa_contratacion = round(random.uniform(20.0, 80.0), 2)
            abandonos = random.randint(0, 10)
            if db_name == "oracle":
                cursor.execute("INSERT INTO INDICADORES_ANALITICOS (id_empresa, id_centro, anio, practicas_realizadas, tasa_finalizacion, satisfaccion_media, tasa_contratacion, abandonos) VALUES (:1, :2, :3, :4, :5, :6, :7, :8)", (id_empresa, id_centro, anio, practicas_realizadas, tasa_finalizacion, satisfaccion_media, tasa_contratacion, abandonos))
            else:
                cursor.execute("INSERT INTO INDICADORES_ANALITICOS (id_empresa, id_centro, anio, practicas_realizadas, tasa_finalizacion, satisfaccion_media, tasa_contratacion, abandonos) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (id_empresa, id_centro, anio, practicas_realizadas, tasa_finalizacion, satisfaccion_media, tasa_contratacion, abandonos))
        commit_fn()
        print(f"{n} indicadores analíticos insertados")

    def insertar_logs_sistema(n=50):
        print(f"Insertando {n} logs del sistema...")
        for _ in range(n):
            id_usuario = random.randint(1, 30)
            tipo_evento = random.choice(['LOGIN', 'LOGOUT', 'INSERT', 'UPDATE', 'DELETE', 'SELECT', 'ERROR', 'WARNING', 'INFO'])
            detalle = fake.text(max_nb_chars=150)
            ip = fake.ipv4()
            if db_name == "oracle":
                cursor.execute("INSERT INTO LOGS_SISTEMA (id_usuario, tipo_evento, detalle, ip) VALUES (:1, :2, :3, :4)", (id_usuario, tipo_evento, detalle, ip))
            else:
                cursor.execute("INSERT INTO LOGS_SISTEMA (id_usuario, tipo_evento, detalle, ip) VALUES (%s, %s, %s, %s)", (id_usuario, tipo_evento, detalle, ip))
        commit_fn()
        print(f"{n} logs del sistema insertados")

    # === EJECUCIÓN ===
    try:
        insertar_centros_educativos(10)
        insertar_empresas(15)
        insertar_estudiantes(30)
        insertar_tutores(15)
        insertar_convenios(20)
        insertar_practicas(40)
        insertar_registros_actividad(100)
        insertar_evaluaciones(50)
        insertar_incidencias(25)
        insertar_documentos(60)
        insertar_indicadores_analiticos(30)
        insertar_logs_sistema(50)

        print(f"\nPOBLACIÓN COMPLETADA: {db_name.upper()}")
        print(f"\nRESUMEN {db_name.upper()}:")
        for tabla in ['CENTROS_EDUCATIVOS', 'EMPRESAS', 'ESTUDIANTES', 'TUTORES', 'CONVENIOS', 'PRACTICAS', 'REGISTROS_ACTIVIDAD', 'EVALUACIONES', 'INCIDENCIAS', 'DOCUMENTOS', 'INDICADORES_ANALITICOS', 'LOGS_SISTEMA']:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            print(f"   • {tabla}: {cursor.fetchone()[0]} registros")
    except Exception as e:
        print(f"ERROR en {db_name}: {e}")
        rollback_fn()
    finally:
        close_fn()

# === MAIN ===
if __name__ == "__main__":
    print("\n" + "="*80)
    print("POBLAR BASES DE DATOS")
    print("="*80 + "\n")

    # Bucle para recorrer todas las BD's y poblarlas con los datos.

    ORACLE_ACTIVE = True
    PG_ACTIVE = True
    MYSQL_ACTIVE = True

    for db, active, connect_fn in [
        ("oracle", "true", lambda: oracledb.connect(user="gestion_practicas", password="gestion123", dsn="localhost/XE")),
        ("postgresql", "true", lambda: psycopg2.connect(host="localhost", user="postgres", password="root", dbname="gestion_practicas")),
        ("mysql", "true", lambda: mysql.connector.connect(host="localhost", user="root", password="root", database="gestion_practicas"))
    ]:
        if active:
            conn = connect_fn()
            cursor = conn.cursor()
            ejecutar_bloque(db, cursor, conn.commit, conn.rollback, lambda: (cursor.close(), conn.close()))