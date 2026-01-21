import re
from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from app.models.abastecimento import TipoCombustivel

class AbastecimentoBase(BaseModel):
    #gt=0 significa maior que zero
    id_posto: int = Field(..., gt=0, description="ID do posto deve ser positivo")
    tipo_combustivel: TipoCombustivel
    preco_por_litro: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    volume_abastecido: float = Field(..., gt=0, description="Volume deve ser maior que zero")
    cpf_motorista: str

class AbastecimentoCreate(AbastecimentoBase):
    #Validador personalizado para limpar e verficar CPF
    @field_validator('cpf_motorista')
    def validar_cpf(cls, v: str):
        #1. Remove tudo que não for número(pontos e traços)
        cpf_limpo = re.sub(r'[^0-9]', '', v)

        #2. Verifica se sobrou algo ou se tem tamanho errado
        if not cpf_limpo or len(cpf_limpo) != 11:
            raise ValueError('CPF inválido: Deve conter 11 digitos numéricos')
        return cpf_limpo
        

class AbastecimentoResponse(AbastecimentoBase):
    id: int
    data_hora: datetime
    improper_data: bool

    class Config:
        from_attributes = True