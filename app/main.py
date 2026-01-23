
from fastapi import FastAPI

from app.api import auth  # 1. Importe o arquivo novo
from app.api import routes

app = FastAPI(
    title="V-Lab Transport API",
    description="API para gestão de abastecimentos",
    version="1.0.0",
)

# Registra as rotas
app.include_router(
    auth.router, prefix="/api/v1"
)  # 2. Adicione esta linha (Login/Signup)
app.include_router(routes.router, prefix="/api/v1")  # Rotas antigas (Abastecimento)


@app.get("/")
async def root():
    return {"status": "ok", "message": "API rodando com sucesso!"}
