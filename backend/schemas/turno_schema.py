from pydantic import BaseModel, EmailStr
from datetime import date, time, datetime
from typing import Optional

class TurnoBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: str
    tipo_turno: str
    fecha: date
    hora: time
    estado: str = "Reservado"
    metodo_pago: str = "Efectivo"
    observaciones: Optional[str] = None

class TurnoCreate(TurnoBase):
    pass

class TurnoSchema(TurnoBase):
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    class Config:
        from_attributes = True

class TurnoOut(TurnoBase):
    id: Optional[int] = None
    created: Optional[datetime] = None
    updated: Optional[datetime] = None

    class Config:
        from_attributes = True