import enum
from datetime import datetime 
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Enum
from app.db.base import Base

class TipoCombustivel(str, enum.Enum):
    GASOLINA = "GASOLINA" 
    ETANOL = "ETANOL"
    DIESEL = "DIESEL"

class Abastecimento(Base):
    __tablename__ = "abastecimentos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_posto = Column(Integer, nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)
    tipo_combustivel = Column(Enum(TipoCombustivel), nullable=False)
    preco_por_litro = Column(Float, nullable=False)
    volume_abastecido = Column(Float, nullable=False)
    cpf_motorista = Column(String, nullable=False)
    improper_data = Column(Boolean, default=False)