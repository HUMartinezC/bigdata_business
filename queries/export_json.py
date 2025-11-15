import json
import oracledb
import psycopg2
import mysql.connector
import os

# ------------------------------
# CONEXIONES HARD-CODEADAS
# ------------------------------
def oracle_conn():
    return oracledb.connect(user="gestion_practicas", password="gestion123", dsn="localhost/XE")

def pg_conn():
    return psycopg2.connect(host="localhost", user="postgres", password="root", dbname="gestion_practicas")

def mysql_conn():
    return mysql.connector.connect(host="localhost", user="root", password="root", database="gestion_practicas")


# =========================
# Directorio para guardar JSON
# =========================
script_dir = os.path.dirname(os.path.abspath(__file__))


# ------------------------------
# ORACLE - CONSULTAS IMPORTANTES
# ------------------------------
def export_oracle():
    conn = oracle_conn()
    cursor = conn.cursor()
    
    # Permite identificar centros con mayor/menor participación
    cursor.execute("""
        SELECT c.nombre, COUNT(e.id_estudiante) as num_estudiantes
        FROM CENTROS_EDUCATIVOS c
        LEFT JOIN ESTUDIANTES e ON e.id_centro = c.id_centro
        GROUP BY c.nombre
    """)
    estudiantes_por_centro = [{ "centro": r[0], "num_estudiantes": r[1] } for r in cursor.fetchall()]
    
    # Muestra el compromiso de las empresas
    cursor.execute("""
        SELECT em.nombre, p.estado, COUNT(*) 
        FROM PRACTICAS p
        JOIN EMPRESAS em ON em.id_empresa = p.id_empresa
        GROUP BY em.nombre, p.estado
    """)
    practicas_por_empresa = [
        { "empresa": r[0], "estado": r[1], "num_practicas": r[2] } 
        for r in cursor.fetchall()
    ]
    
    # Muestra la satisfacción media de las empresas
    cursor.execute("""
        SELECT em.nombre, AVG(p.evaluacion_final) 
        FROM PRACTICAS p
        JOIN EMPRESAS em ON em.id_empresa = p.id_empresa
        GROUP BY em.nombre
    """)
    satisfaccion_empresas = [
        { "empresa": r[0], "satisfaccion_media": float(r[1]) if r[1] is not None else None } 
        for r in cursor.fetchall()
    ]
    
    data = {
        "estudiantes_por_centro": estudiantes_por_centro,
        "practicas_por_empresa": practicas_por_empresa,
        "satisfaccion_empresas": satisfaccion_empresas
    }
    
    file_path = os.path.join(script_dir, "oracle_data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    cursor.close()
    conn.close()

# ------------------------------
# POSTGRESQL - CONSULTAS IMPORTANTES
# ------------------------------
def export_postgresql():
    conn = pg_conn()
    cursor = conn.cursor()
    
    # Permite obtener la cantidad de tutores por centro educativo
    cursor.execute("""
        SELECT c.nombre, COUNT(t.id_tutor)
        FROM centros_educativos c
        LEFT JOIN tutores t ON t.id_centro = c.id_centro
        GROUP BY c.nombre
    """)
    tutores_por_centro = [{"centro": r[0], "num_tutores": r[1]} for r in cursor.fetchall()]
    
    # Mide la tasa de prácticas finalizadas por empresa
    cursor.execute("""
        SELECT e.nombre, COUNT(p.id_practica)
        FROM empresas e
        JOIN practicas p ON p.id_empresa = e.id_empresa
        WHERE p.estado = 'finalizada'
        GROUP BY e.nombre
    """)
    practicas_finalizadas = [{"empresa": r[0], "num_finalizadas": r[1]} for r in cursor.fetchall()]
    
    # Mide la cantidad de incidencias por práctica
    cursor.execute("""
        SELECT p.id_practica, COUNT(i.id_incidencia)
        FROM practicas p
        LEFT JOIN incidencias i ON i.id_practica = p.id_practica
        GROUP BY p.id_practica
    """)
    incidencias_por_practica = [{"id_practica": r[0], "num_incidencias": r[1]} for r in cursor.fetchall()]
    
    data = {
        "tutores_por_centro": tutores_por_centro,
        "practicas_finalizadas": practicas_finalizadas,
        "incidencias_por_practica": incidencias_por_practica
    }
    
    file_path = os.path.join(script_dir, "postgresql_data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    cursor.close()
    conn.close()

# ------------------------------
# MYSQL - CONSULTAS IMPORTANTES
# ------------------------------
def export_mysql():
    conn = mysql_conn()
    cursor = conn.cursor()
    
    # Mide el número de convenios por empresa
    cursor.execute("""
        SELECT e.nombre, COUNT(c.id_convenio)
        FROM EMPRESAS e
        LEFT JOIN CONVENIOS c ON c.id_empresa = e.id_empresa
        GROUP BY e.nombre
    """)
    convenios_por_empresa = [{"empresa": r[0], "num_convenios": r[1]} for r in cursor.fetchall()]
    
    # Evaluar cumplimiento de requisitos (documentación, presentaciones, etc.)
    cursor.execute("""
        SELECT p.id_practica, COUNT(d.id_documento)
        FROM PRACTICAS p
        LEFT JOIN DOCUMENTOS d ON d.id_practica = p.id_practica
        GROUP BY p.id_practica
    """)
    documentos_por_practica = [{"id_practica": r[0], "num_documentos": r[1]} for r in cursor.fetchall()]
    
    # Evaluaciones promedio por práctica para obtener desempeño de los estudiantes
    cursor.execute("""
        SELECT p.id_practica, AVG(e.puntuacion)
        FROM PRACTICAS p
        LEFT JOIN EVALUACIONES e ON e.id_practica = p.id_practica
        GROUP BY p.id_practica
    """)
    evaluaciones_por_practica = [{"id_practica": r[0], "puntuacion_media": float(r[1]) if r[1] else None} for r in cursor.fetchall()]
    
    data = {
        "convenios_por_empresa": convenios_por_empresa,
        "documentos_por_practica": documentos_por_practica,
        "evaluaciones_por_practica": evaluaciones_por_practica
    }
    
    file_path = os.path.join(script_dir, "mysql_data.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    cursor.close()
    conn.close()

# ------------------------------
# MAIN
# ------------------------------
if __name__ == "__main__":
    export_oracle()
    export_postgresql()
    export_mysql()
    print("¡JSONs generados correctamente para cada base de datos!")


# =========================
# Conclusión
# =========================

"""
El script exporta datos importantes de cada base de datos para analizar rendimiento, detectar problemas y tomar decisiones para mejorar la gestión de prácticas.

Se han exportado los siguientes datos:
- Oracle: estudiantes por centro, prácticas por empresa y satisfacción empresas.
- PostgreSQL: tutores por centro, prácticas finalizadas y incidencias por práctica.
- MySQL: convenios por empresa, documentos por práctica y evaluaciones por práctica.
"""