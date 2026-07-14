from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from datetime import date
from db.dependencies import get_db
from schemas.turno_schema import TurnoCreate, TurnoSchema, TurnoOut
from services.turno_service import (
    get_turnos,
    get_turno,
    create_turno,
    update_turno,
    delete_turno,
    get_all_turnos_paginated,
    get_horarios_ocupados,
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/turnos", tags=["Turnos"])

# IMPORTANTE: las rutas con texto fijo (/paginado, /ocupados) van ANTES que /{id},
# porque FastAPI matchea en orden y si no, "paginado"/"ocupados" se interpretarían
# como si fueran un id numérico y tirarían error 422.

@router.get("/", response_model=List[TurnoOut])
def listar_turnos(session: Session = Depends(get_db)):
    return get_turnos(session)

@router.get("/paginado", response_model=List[TurnoOut])
def turnos_paginado(skip: int = 0, limit: int = 15, session: Session = Depends(get_db)):
    return get_all_turnos_paginated(session, skip=skip, limit=limit)

@router.get("/ocupados")
def horarios_ocupados(fecha: date, session: Session = Depends(get_db)):
    """Devuelve la lista de horarios (HH:MM) ya reservados para una fecha dada."""
    return {"fecha": str(fecha), "horarios": get_horarios_ocupados(session, fecha)}

@router.get("/{id}", response_model=TurnoSchema)
def obtener_turno(id: int, session: Session = Depends(get_db)):
    turno = get_turno(session, id)
    if turno:
        return turno
    else:
        return JSONResponse(content={"error": "Turno no encontrado"}, status_code=404)

from services.email_service import enviar_confirmacion_turno

@router.post("/", response_model=TurnoSchema, status_code=201)
def crear_turno(turno: TurnoCreate, session: Session = Depends(get_db)):
    try:
        nuevo_turno = create_turno(session, turno)
        enviar_confirmacion_turno(nuevo_turno)
        return nuevo_turno
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.put("/{id}", response_model=TurnoSchema)
def actualizar_turno(id: int, turno: TurnoCreate, session: Session = Depends(get_db)):
    updated = update_turno(session, id, turno)
    if updated:
        return updated
    else:
        return JSONResponse(content={"error": "Turno no encontrado"}, status_code=404)

@router.delete("/{id}")
def eliminar_turno(id: int, session: Session = Depends(get_db)):
    deleted = delete_turno(session, id)
    if deleted:
        return {"message": "Turno eliminado"}
    else:
        return JSONResponse(content={"error": "Turno no encontrado"}, status_code=404)