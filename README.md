# 📦 DB Migration API (Departments, Jobs, Employees)

Este proyecto implementa una **API REST** con **FastAPI** para simular un proceso real de **migración de datos** desde archivos CSV hacia una base de datos SQL.

## 🚀 Objetivo

En el contexto de una migración con tres tablas principales:

- **Departments**
- **Jobs**
- **Hired Employees**

La API permite:

1. 📥 **Recibir datos históricos** desde archivos CSV.
2. 💾 **Cargar estos datos** en una base de datos SQL.
3. ⚡ **Insertar transacciones en lote** (de **1** a **2000 registros** por petición) optimizando el rendimiento.

---

## 🛠️ Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI** (framework para API REST)
- **SQLAlchemy** (ORM para manejo de base de datos)
- **MySQL** o **SQLite** (configurable)
- **Pandas** (procesamiento de CSV)
- **Uvicorn** (servidor ASGI)

---

## 📂 Estructura del proyecto

```bash
.
├── app/
│   ├── api/            # Endpoints de la API
│   ├── core/           # Configuración general (DB, settings)
│   ├── crud/           # Funciones CRUD para BD
│   ├── models/         # Modelos de SQLAlchemy
│   ├── schemas/        # Esquemas Pydantic para validación
│   ├── main.py         # Punto de entrada de la API
│
├── archivos/           # Archivos CSV de entrada
├── venv/               # Entorno virtual (excluido en Git)
├── main.ipynb          # Notebook para pruebas
├── README.md           # Documentación del proyecto
├── requirements.txt    # Dependencias del proyecto
└── .gitignore
