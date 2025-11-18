from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from db.init_db import init_db
from datetime import datetime, time
from routers import turno_router
app = FastAPI()

# Configuración de CORS
origins = [
    "http://127.0.0.1:3002", # Tu frontend local
    "http://localhost:3002",
    "https://127.0.0.1:5500",
    "https://localhost:5500"
    # Agrega aquí cualquier otro origen donde se despliegue tu frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Inicializar base de datos ANTES de incluir routers
init_db()  # ✅ Llamar directamente aquí

# # Función de validación de hora
# def validar_hora(hora_str: str):
#     try:
#         h = datetime.strptime(hora_str, "%H:%M").time()
#         # Validar que la hora sea en bloques de 30 minutos
#         if h.minute not in [0, 30]:
#             raise ValueError("La hora debe ser en bloques de 30 minutos (ej. 10:00, 10:30).")

#         # Validar rango de horas
#         if not (time(9, 0) <= h <= time(12, 0) or time(15, 0) <= h <= time(20, 30)):
#             raise ValueError("La hora debe estar entre 09:00 y 12:00 o entre 15:00 y 20:30.")
#         return True
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# Rutas de la API
app.include_router(turno_router.router)

import uvicorn
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)