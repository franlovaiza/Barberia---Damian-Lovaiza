from backend.db.database import Base, engine
from backend.db.models.turno_model import Turno

async def init_db():
    Base.metadata.create_all(bind=engine)
