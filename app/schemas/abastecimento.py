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
        cpf = re.sub(r'[^0-9]', '', v)

        #2. Chegacagem primária: Tamanho e sequência repetias
        if len(cpf) !=11 or cpf == cpf[0] * len(cpf):
            raise ValueError('CPF inválido: Formato incorreto')
        
        #3. Cálculo do 1 digito verificador
        soma = sum(int(cpf[i]) * (10-i) for i in range(9))
        resto = (soma * 10 ) % 11
        if resto == 10: resto = 0
        if resto != int(cpf[9]):
            raise ValueError('CPF inválido: Digitos verificadores não conferem')
        
        #4. Calculo do 2 digito verificador
        soma = sum(int(cpf[i]) * (11-i) for i in range(10))
        resto = (soma * 10) % 11
        if resto == 10: resto = 0
        if resto != int(cpf[10]):
            raise ValueError('CPF inválido: Dígitos verificadores não conferem')
        return cpf
        

class AbastecimentoResponse(AbastecimentoBase):
    id: int
    data_hora: datetime
    improper_data: bool

    class Config:
        from_attributes = True