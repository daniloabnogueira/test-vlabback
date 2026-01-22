from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.base import Base
from app.db.session import engine
from app.api import routes
from app.api import auth  # 1. Importe o arquivo novo

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Cria as tabelas ao iniciar (incluindo a de usuários agora)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="V-Lab Transport API",
    description="API para gestão de abastecimentos",
    version="1.0.0",
    lifespan=lifespan
)

# Registra as rotas
app.include_router(auth.router, prefix="/api/v1")     # 2. Adicione esta linha (Login/Signup)
app.include_router(routes.router, prefix="/api/v1")   # Rotas antigas (Abastecimento)

@app.get("/")
async def root():
    return {"status": "ok", "message": "API rodando com sucesso!"}