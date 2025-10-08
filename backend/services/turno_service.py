from sqlalchemy.orm import Session
from backend.db.models.turno_model import Turno
from backend.schemas.turno_schema import TurnoCreate, TurnoSchema, TurnoOut
from typing import List, Optional

def get_all_turnos_paginated(db: Session, skip: int = 0, limit: int = 15) -> List[TurnoOut]:
    turnos = db.query(Turno).offset(skip).limit(limit).all()
    return [TurnoOut(**t.__dict__) for t in turnos]

def get_turnos(db: Session) -> List[TurnoOut]:
    turnos = db.query(Turno).all()
    return [TurnoOut(**t.__dict__) for t in turnos]

def get_turno(db: Session, turno_id: int) -> Optional[TurnoSchema]:
    turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if turno:
        return TurnoSchema(**turno.__dict__)
    return None

def create_turno(db: Session, turno: TurnoCreate) -> TurnoSchema:
    db_turno = Turno(**turno.dict())
    db.add(db_turno)
    db.commit()
    db.refresh(db_turno)
    return TurnoSchema(**db_turno.__dict__)

def update_turno(db: Session, turno_id: int, turno_update: TurnoCreate) -> Optional[TurnoSchema]:
    db_turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not db_turno:
        return None
    for field, value in turno_update.dict().items():
        setattr(db_turno, field, value)
    db.commit()
    db.refresh(db_turno)
    return TurnoSchema(**db_turno.__dict__)

def delete_turno(db: Session, turno_id: int) -> bool:
    db_turno = db.query(Turno).filter(Turno.id == turno_id).first()
    if not db_turno:
        return False
    db.delete(db_turno)
    db.commit()
    return True


