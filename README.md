# Sistema de Gestión de Prácticas

Proyecto para la gestión de prácticas profesionales con soporte multi-base de datos (MySQL, PostgreSQL, Oracle) y herramientas de administración de datos.

## 📁 Estructura del Proyecto

```
gestion_practicas/
├── docker/                  # Configuración Docker
│   ├── docker-compose.yml   # Orquestación de contenedores
│   ├── Dockerfile-mysql     # Imagen MySQL
│   ├── Dockerfile-postgres  # Imagen PostgreSQL
│   └── Dockerfile-oracle    # Imagen Oracle
├── python/                  # Scripts Python
│   ├── crear_bds.py        # Creación de bases de datos
│   └── seed.py             # Población con datos de prueba
├── queries/                 # Consultas y exportaciones
│   ├── export_json.py      # Exportación a JSON
├── sql/                     # Scripts SQL
│   ├── MySQL_Script_Gestion_Practicas.sql
│   ├── Oracle_Script_Gestion_Practicas.sql
│   ├── PostgreSQL_BD_Script_Gestion_Practicas.sql
│   └── PostgreSQL_Tablas_Script_Gestion_Practicas.sql
└── requirements.txt         # Dependencias Python
```

## Características Principales

- **Multi-base de datos**: Soporte para MySQL, PostgreSQL y Oracle
- **Contenerización**: Configuración Docker para despliegue fácil
- **Datos de prueba**: Scripts para generar datos aleatorios con Faker
- **Exportación de datos**: Herramientas para exportar a formato JSON
- **Gestión completa**: Sistema completo para gestión de prácticas profesionales

## Tecnologías Utilizadas

- **Bases de datos**: MySQL, PostgreSQL 16+, Oracle
- **Contenerización**: Docker & Docker Compose
- **Lenguajes**: SQL, Python
- **Librerías Python**: 
  - `mysql-connector-python`
  - `psycopg2-binary`
  - `oracledb`
  - `faker`

## Requisitos Previos

- Docker y Docker Compose instalados
- Python 3.8+
- Entorno virtual configurado

## Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd gestion_practicas
```

### 2. Configurar entorno virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate     # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Iniciar bases de datos con Docker
```bash
cd docker
docker-compose up -d
```

## Modelo de Datos

El sistema gestiona las siguientes entidades principales:

- **Estudiantes**: Información de los estudiantes en prácticas
- **Empresas**: Datos de las empresas
- **Centros educativos**: Centros educativos
- **Tutores**: Tutores académicos y empresariales
- **Convenios**: Acuerdos entre instituciones y empresas
- **Prácticas**: Asignaciones y seguimiento de prácticas
- **Evaluaciones**: Sistema de evaluación de desempeño
- **Incidencias**: Registro de incidencias durante las prácticas
- **Documentos**: Gestión documental
- **Indicadores**: Métricas y análisis
- **Logs**: Registro de actividad del sistema
- **Registros de actividad**: Registro de actividades realizadas por los usuarios

## Scripts SQL

### Scripts disponibles:
- `MySQL_Script_Gestion_Practicas.sql` - Creación completa para MySQL
- `Oracle_Script_Gestion_Practicas.sql` - Creación completa para Oracle
- `PostgreSQL_BD_Script_Gestion_Practicas.sql` - Creación BD PostgreSQL
- `PostgreSQL_Tablas_Script_Gestion_Practicas.sql` - Tablas PostgreSQL

## Scripts Python

### `crear_bds.py`
Script para la creación automática de las bases de datos en los diferentes motores.

### `seed.py`
Genera datos de prueba aleatorios utilizando Faker con 10 providers:
- name, address, phone_number, email, date_of_birth
- company, company_email, text, country, date_between

### `export_json.py`
Exporta datos de las bases de datos a formato JSON para análisis o migración.

## Configuración Docker

### Servicios configurados:
- **MySQL**: Puerto 3306, contraseña: root
- **PostgreSQL**: Puerto 5432 
- **Oracle**: Puerto 1521

### Variables de entorno:
```yaml
MYSQL_ROOT_PASSWORD: 
MYSQL_DATABASE: 

POSTGRES_USER: 
POSTGRES_PASSWORD: 
POSTGRES_DB: 

ORACLE_PASSWORD: 
```

## Uso

### 1. Levantar contenedores
```bash
cd docker
docker-compose up -d
```

### 2. Crear bases de datos
```bash
cd python
python crear_bds.py
```

### 3. Poblar con datos de prueba
```bash
python seed.py
```

### 4. Exportar datos
```bash
cd queries
python export_json.py
```

## Consultas y Análisis

Los datos exportados en JSON están disponibles en:
- `queries/mysql_data.json`
- `queries/oracle_data.json` 
- `queries/postgresql_data.json`

---

**Desarrollado para el curso de IA y Big Data - Sistema de Big Data**
