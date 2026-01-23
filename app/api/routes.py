from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.abastecimento import Abastecimento, TipoCombustivel
from app.models.usuario import Usuario
from app.schemas.abastecimento import (AbastecimentoCreate,
                                       AbastecimentoResponse)
# Importa o Service novo 👇
from app.services.abastecimento import AbastecimentoService

router = APIRouter()


@router.post("/abastecimentos/", response_model=AbastecimentoResponse, status_code=201)
async def create_abastecimento(
    abastecimento_in: AbastecimentoCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    # Delega a lógica complexa (Média do banco + 25%) para o Service
    service = AbastecimentoService(db)
    return await service.create(abastecimento_in)


@router.get("/abastecimentos/", response_model=List[AbastecimentoResponse])
async def list_abastecimentos(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Itens por página"),
    tipo_combustivel: Optional[TipoCombustivel] = None,
    db: AsyncSession = Depends(get_db),
):
    # Query base
    query = select(Abastecimento)

    # Filtros
    if tipo_combustivel:
        query = query.where(Abastecimento.tipo_combustivel == tipo_combustivel)

    # Paginação
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/motorista/{cpf}/historico", response_model=List[AbastecimentoResponse])
async def get_historico_motorista(cpf: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Abastecimento).where(Abastecimento.cpf_motorista == cpf)
    )
    abastecimentos = result.scalars().all()

    # Retornar lista vazia se não achar nada é um padrão REST aceitável
    if not abastecimentos:
        return []

    return abastecimentos
