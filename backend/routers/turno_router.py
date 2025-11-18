from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from typing import List, Optional
from db.dependencies import get_db
from schemas.turno_schema import TurnoCreate, TurnoSchema, TurnoOut
from services.turno_service import (
    get_turnos,
    get_turno,
    create_turno,
    update_turno,
    delete_turno,
    get_all_turnos_paginated
)
from sqlalchemy.orm import Session

router = APIRouter(prefix="/turnos", tags=["Turnos"])

@router.get("/", response_model=List[TurnoOut])
def listar_turnos(session: Session = Depends(get_db)):
    return get_turnos(session)

@router.get("/{id}", response_model=TurnoSchema)
def obtener_turno(id: int, session: Session = Depends(get_db)):
    turno = get_turno(session, id)
    if turno:
        return turno
    else:
        return JSONResponse(content={"error": "Turno no encontrado"}, status_code=404)

@router.post("/", response_model=TurnoSchema, status_code=201)
async def crear_turno(turno: TurnoCreate, session: Session = Depends(get_db)):
    # create_turno es una coroutine (usa envío de mail async), debe awaitearse
    return await create_turno(session, turno)

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

@router.get("/paginado", response_model=List[TurnoOut])
def turnos_paginado(skip: int = 0, limit: int = 15, session: Session = Depends(get_db)):
    return get_all_turnos_paginated(session, skip=skip, limit=limit)