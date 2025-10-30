from .database import Base, engine
from .models.turno_model import Turno

def init_db():  # Quitar async
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada")  # Para confirmar que se ejecutó