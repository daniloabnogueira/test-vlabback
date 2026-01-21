from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoResponse

router = APIRouter()

@router.post("/abastecimentos/", response_model=AbastecimentoResponse, status_code=201)
async def create_abastecimento(
    abastecimento_in: AbastecimentoCreate,
    db: AsyncSession = Depends(get_db)
):
    #1. Transformar o Schema (Pydantic) em Model (SQLAlchemy)
    # O model_dump converte o imput em um dicionário python
    novo_abastecimento = Abastecimento(**abastecimento_in.model_dump())

    #2. Adiciona no banco
    db.add(novo_abastecimento)

    #3. Salvar (commit) e atualizar (Refresh para pegar o ID gerado pelo banco)
    await db.commit()
    await db.refresh(novo_abastecimento)

    return novo_abastecimento

@router.get("/abastecimentos/", response_model=list[AbastecimentoResponse])
async def list_abastecimentos(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Abastecimento))
    return result.scalars().all()