from pydantic import BaseModel, ConfigDict

# O que a API devolve quando alguém loga com sucesso
class Token(BaseModel):
    access_token: str
    token_type: str

# Dados dentro do token
class TokenData(BaseModel):
    username: str | None = None

# Base para cadastro e leitura
class UsuarioBase(BaseModel):
    username: str

# Para criar, precisamos da senha
class UsuarioCreate(UsuarioBase):
    password: str

# Para devolver ao front-end (NUNCA devolvemos a senha)
class UsuarioResponse(UsuarioBase):
    id: int
    model_config = ConfigDict(from_attributes=True)