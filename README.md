# Proyecto Centro de Salud - Base de Datos Avanzadas

Aplicación funcional en Python + Streamlit conectada a MySQL para consultar los 4 reportes solicitados en el proyecto.

## Tecnologías

- MySQL 8.x
- Python 3.10+
- Streamlit
- mysql-connector-python
- pandas
- python-dotenv

## Instalación rápida

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Copia `.env.example` como `.env` y ajusta tus credenciales:

```bash
copy .env.example .env
```

Ejecuta los scripts SQL en MySQL Workbench en este orden:

1. `database/01_schema.sql`
2. `database/02_seed.sql`
3. `database/03_views_procedures_triggers.sql`

Luego ejecuta la app:

```bash
streamlit run app/main.py
```
