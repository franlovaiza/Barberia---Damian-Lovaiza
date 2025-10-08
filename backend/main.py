from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime, time

app = FastAPI()

# Configuración de CORS
origins = [
    "http://127.0.0.1:3002", # Tu frontend local
    "http://localhost:3002",
    # Agrega aquí cualquier otro origen donde se despliegue tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "database.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row # Para acceder a las columnas por nombre
    return conn

# Inicializar la base de datos
@app.on_event("startup")
def startup_event():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Función de validación de hora
def validar_hora(hora_str: str):
    try:
        h = datetime.strptime(hora_str, "%H:%M").time()
        # Validar que la hora sea en bloques de 30 minutos
        if h.minute not in [0, 30]:
            raise ValueError("La hora debe ser en bloques de 30 minutos (ej. 10:00, 10:30).")

        # Validar rango de horas
        if not (time(9, 0) <= h <= time(12, 0) or time(15, 0) <= h <= time(20, 30)):
            raise ValueError("La hora debe estar entre 09:00 y 12:00 o entre 15:00 y 20:30.")
        return True
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Esquema para el turno (puedes usar Pydantic para esto, pero para simplicidad, lo manejamos manualmente)
class Turno:
    def __init__(self, nombre: str, telefono: str, fecha: str, hora: str):
        self.nombre = nombre
        self.telefono = telefono
        self.fecha = fecha
        self.hora = hora

# Rutas de la API
@app.post("/turnos/")
async def crear_turno(turno: dict):
    nombre = turno.get("nombre")
    telefono = turno.get("telefono")
    fecha = turno.get("fecha")
    hora = turno.get("hora")

    if not all([nombre, telefono, fecha, hora]):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    validar_hora(hora)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si ya existe un turno para la misma fecha y hora
    cursor.execute("SELECT * FROM turnos WHERE fecha = ? AND hora = ?", (fecha, hora))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Ya existe un turno para esta fecha y hora.")

    try:
        cursor.execute("INSERT INTO turnos (nombre, telefono, fecha, hora) VALUES (?, ?, ?, ?)",
                        (nombre, telefono, fecha, hora))
        conn.commit()
        conn.close()
        return {"message": "Turno creado exitosamente"}
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error al crear turno: {e}")

@app.get("/turnos/")
async def obtener_turnos(nombre: str = Query(None), telefono: str = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT id, nombre, telefono, fecha, hora FROM turnos"
    params = []

    conditions = []
    if nombre:
        conditions.append("nombre LIKE ?")
        params.append(f"%{nombre}%") # Búsqueda parcial
    if telefono:
        conditions.append("telefono LIKE ?")
        params.append(f"%{telefono}%") # Búsqueda parcial

    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    # Ordenar por fecha y hora para una mejor visualización
    query += " ORDER BY fecha, hora"

    cursor.execute(query, tuple(params))
    turnos = cursor.fetchall()
    conn.close()
    
    # Convertir Row objects a listas o diccionarios para la respuesta JSON
    turnos_list = [list(turno) for turno in turnos]
    return {"turnos": turnos_list}


@app.put("/turnos/{turno_id}")
async def actualizar_turno(turno_id: int, turno: dict):
    nombre = turno.get("nombre")
    telefono = turno.get("telefono")
    fecha = turno.get("fecha")
    hora = turno.get("hora")

    if not all([nombre, telefono, fecha, hora]):
        raise HTTPException(status_code=400, detail="Todos los campos son obligatorios.")

    validar_hora(hora)

    conn = get_db_connection()
    cursor = conn.cursor()

    # Verificar si el turno existe
    cursor.execute("SELECT * FROM turnos WHERE id = ?", (turno_id,))
    if not cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Turno no encontrado.")

    # Verificar si ya existe otro turno para la misma fecha y hora (excluyendo el turno actual)
    cursor.execute("SELECT * FROM turnos WHERE fecha = ? AND hora = ? AND id != ?", (fecha, hora, turno_id))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=409, detail="Ya existe otro turno para esta fecha y hora.")

    try:
        cursor.execute("UPDATE turnos SET nombre = ?, telefono = ?, fecha = ?, hora = ? WHERE id = ?",
                        (nombre, telefono, fecha, hora, turno_id))
        conn.commit()
        conn.close()
        return {"message": "Turno actualizado exitosamente"}
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error al actualizar turno: {e}")

@app.delete("/turnos/{turno_id}")
async def eliminar_turno(turno_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM turnos WHERE id = ?", (turno_id,))
        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Turno no encontrado.")
        conn.commit()
        conn.close()
        return {"message": "Turno eliminado exitosamente"}
    except sqlite3.Error as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Error al eliminar turno: {e}")

import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)