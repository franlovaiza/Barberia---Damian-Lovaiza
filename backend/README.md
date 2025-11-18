# Backend - Barbería DL

Este README describe cómo configurar y ejecutar el backend de la API de turnos.

## Resumen

Proyecto sencillo con FastAPI + SQLAlchemy que expone endpoints para gestionar turnos (crear, listar, actualizar y eliminar).

Estructura relevante:

- `main.py` - punto de entrada de la aplicación (inicializa la BD y monta routers).
- `db/` - configuración y modelos de la base de datos.
- `routers/turno_router.py` - endpoints relacionados con los turnos.
- `services/turno_service.py` - lógica de negocio para turnos.
- `schemas/turno_schema.py` - modelos Pydantic para validación.
- `.env` - variables de entorno (no incluir en VCS con secretos reales).
- `requirements.txt` - dependencias del backend.

---

## Requisitos

- Python 3.11+ (se probó con 3.11/3.12)
- Windows PowerShell (instrucciones incluidas más abajo)

> Nota: el proyecto usa SQLite por defecto (`DATABASE_URL=sqlite:///./database.db` en `.env`), así que no necesitas instalar drivers adicionales para desarrollo.

---

## Configuración (Windows PowerShell)

1. Crear y activar un entorno virtual:

```powershell
cd path\to\Barberia---Damian-Lovaiza\backend
python -m venv .venv
# Activar (PowerShell)
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

3. Variables de entorno

El proyecto ya incluye un archivo `.env` de ejemplo en el directorio `backend`. Asegúrate de revisarlo y actualizar valores sensibles si fuese necesario.

Parámetros importantes en `.env`:

- `API_URL` - URL base de la API (ej. `http://localhost:8000`)
- `FRONTEND_URL` - URL del frontend
- `DATABASE_URL` - por defecto `sqlite:///./database.db`
- `TOKEN_SECRET` - clave secreta para tokens (si se usa autenticación)
- `TOKEN_HOURS_DURATION` - duración del token en horas

El proyecto usa `pydantic-settings` para cargar `.env` automáticamente desde `backend/config.py`.

---

## Inicializar la base de datos

La creación de tablas se ejecuta automáticamente desde `main.py` al importar `init_db()`:

- `db/init_db.py` llama a `Base.metadata.create_all(bind=engine)`.

Si necesitas reiniciar la base (eliminar `database.db` y crear tablas desde cero):

```powershell
# Desde backend/
Remove-Item .\database.db -ErrorAction Ignore
python -c "from db.init_db import init_db; init_db()"
```

---

## Ejecutar la aplicación (desarrollo)

Ejecuta Uvicorn desde el directorio `backend`:

```powershell
# Activar venv previamente
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

La API quedará disponible en `http://127.0.0.1:8000`.

---

## Endpoints principales

- GET `/turnos/` — Lista todos los turnos.
- GET `/turnos/{id}` — Obtiene un turno por id.
- POST `/turnos/` — Crea un turno.
- PUT `/turnos/{id}` — Actualiza un turno.
- DELETE `/turnos/{id}` — Elimina un turno.
- GET `/turnos/paginado?skip=0&limit=15` — Lista paginada.

Ejemplo de body para crear un turno (JSON):

```json
{
  "nombre": "Juan Pérez",
  "email": "juan@example.com",
  "telefono": "123456789",
  "tipo_turno": "Corte",
  "fecha": "2025-10-31",
  "hora": "10:30:00",
  "observaciones": "Corte clásico"
}
```

> Nota: el campo `hora` en los schemas se valida como `time` en Pydantic; internamente se guarda como string `HH:MM:SS` para compatibilidad con el modelo SQLAlchemy.

---

## Uso rápido con curl (ejemplos)

Crear un turno:

```powershell
curl -X POST "http://127.0.0.1:8000/turnos/" -H "Content-Type: application/json" -d @- <<'JSON'
{
  "nombre": "Prueba",
  "email": "prueba@example.com",
  "telefono": "999999999",
  "tipo_turno": "Barba",
  "fecha": "2025-10-31",
  "hora": "15:00:00"
}
JSON
```

Listar turnos:

```powershell
curl http://127.0.0.1:8000/turnos/
```

---

## Recomendaciones / próximos pasos

- Fijar versiones en `requirements.txt` (recomendado) para garantizar reproducibilidad.
- Añadir tests unitarios para servicios y routers.
- Si se despliega a producción con PostgreSQL, añadir `psycopg2-binary` y actualizar `DATABASE_URL`.
- Habilitar CORS sólo para las URLs necesarias en producción.

---

Si quieres, puedo:

- Fijar versiones exactas en `requirements.txt`.
- Añadir un `Makefile` o scripts PowerShell para tareas comunes (crear venv, instalar deps, ejecutar).
- Generar un pequeño `curl`/Insomnia collection para probar la API.

