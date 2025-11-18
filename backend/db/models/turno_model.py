from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.database import Base

class Turno(Base):
    __tablename__ = "turno"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(60))
    email = Column(String(100))
    telefono = Column(String(15))
    tipo_turno = Column(String(25))
    fecha = Column(DateTime)
    hora = Column(String(10))
    estado = Column(String(20), default="Reservado")
    observaciones = Column(String(200), nullable=True)

    # Timestamps
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())