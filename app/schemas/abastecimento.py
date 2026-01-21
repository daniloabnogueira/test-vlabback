from datetime import datetime
from pydantic import BaseModel, Field
from app.models.abastecimento import TipoCombustivel

class AbastecimentoBase(BaseModel):
    id_posto: int
    tipo_combustivel: TipoCombustivel
    preco_por_litro: float
    volume_abastecido: float
    cpf_motorista: str

class AbastecimentoCreate(AbastecimentoBase):
    pass

class AbastecimentoResponse(AbastecimentoBase):
    id: int
    data_hora: datetime
    improper_data: bool

    class Config:
        from_attributes = True