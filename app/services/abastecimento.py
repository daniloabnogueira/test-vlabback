from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.abastecimento import Abastecimento
from app.schemas.abastecimento import AbastecimentoCreate


class AbastecimentoService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, abastecimento_in: AbastecimentoCreate):
        """
        Cria um novo abastecimento aplicando a regra de negócio de anomalia.
        Regra: Se o preço for > 25% da média histórica, marca como improper_data.
        """

        # 1. Busca a Média Histórica REAL no Banco de Dados para este combustível
        query_media = select(func.avg(Abastecimento.preco_por_litro)).where(
            Abastecimento.tipo_combustivel == abastecimento_in.tipo_combustivel
        )
        resultado = await self.db.execute(query_media)
        media_preco = resultado.scalar()  # Retorna None se não houver registros

        is_anomalia = False

        # 🛡️ PROTEÇÃO (Cold Start): Só aplicamos a regra se JÁ existir histórico
        if media_preco is not None:
            # Regra: Preço > Média + 25% (fator 1.25)
            limite_aceitavel = float(media_preco) * 1.25

            if abastecimento_in.preco_por_litro > limite_aceitavel:
                is_anomalia = True

        # Nota: Se media_preco for None (primeiro registro), is_anomalia continua False.
        # O sistema aceita o primeiro valor como "a verdade" inicial para formar a média.

        # 2. Prepara o objeto para salvar
        novo_abastecimento = Abastecimento(
            **abastecimento_in.model_dump(), improper_data=is_anomalia
        )

        # 3. Salva no Banco
        self.db.add(novo_abastecimento)
        await self.db.commit()
        await self.db.refresh(novo_abastecimento)

        return novo_abastecimento
