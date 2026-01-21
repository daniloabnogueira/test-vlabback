from typing import Optional
from datetime import date
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.db.session import get_db
from app.models.abastecimento import Abastecimento, TipoCombustivel
from app.schemas.abastecimento import AbastecimentoCreate, AbastecimentoResponse

router = APIRouter()

MEDIAS_PRECO = {
    TipoCombustivel.GASOLINA: 5.50,
    TipoCombustivel.ETANOL: 3.80,
    TipoCombustivel.DIESEL: 6.00
}
@router.post("/abastecimentos/", response_model=AbastecimentoResponse, status_code=201)
async def create_abastecimento(
    abastecimento_in: AbastecimentoCreate,
    db: AsyncSession = Depends(get_db)
):
    #1. Transformar o Schema (Pydantic) em Model (SQLAlchemy)
    # O model_dump converte o imput em um dicionário python
    novo_abastecimento = Abastecimento(**abastecimento_in.model_dump())

    #Regra de Negócio: Anomalia de Preço (>media + 25%)
    #Busca acontece baseada na média do tipo de combustível enviado
    media_historica = MEDIAS_PRECO.get(abastecimento_in.tipo_combustivel)

    #Calculamos o teto aceitavel
    limite_aceitavel = media_historica * 1.25

    if abastecimento_in.preco_por_litro > limite_aceitavel:
        novo_abastecimento.improper_data = True
    else:
        novo_abastecimento.improper_data = False

    #2. Adiciona no banco
    db.add(novo_abastecimento)

    #3. Salvar (commit) e atualizar (Refresh para pegar o ID gerado pelo banco)
    await db.commit()
    await db.refresh(novo_abastecimento)

    return novo_abastecimento

@router.get("/abastecimentos/", response_model=list[AbastecimentoResponse])
async def list_abastecimentos(
    page: int = Query(1, ge=1, description="Número da página (min:1)"),
    size: int = Query(10, ge=1, le=100, description="Itens por página (max: 100)"),
    tipo_combustivel: Optional[TipoCombustivel] = None,
    db: AsyncSession = Depends(get_db)
):
    #Base da Query
    query = select(Abastecimento)

    #Aplicar filtro de combustivel (se foi mandado pelo usuario)
    if tipo_combustivel:
        query = query.where(Abastecimento.tipo_combustivel == tipo_combustivel)
    
    #Paginação (pular os itens das páginas anteriores)
    offset = (page - 1) * size
    query = query.offset(offset).limit(size)

   #Executar
    result = await db.execute(query)

    return result.scalars().all()