import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app

BASE_URL = "http://test"


# --- FIXTURE: O "Crachá" para os testes ---
@pytest.fixture
async def token_autenticado():
    """
    1. Cria um usuário de teste.
    2. Faz login.
    3. Retorna o cabeçalho 'Authorization' pronto para uso.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        # Tenta criar usuário (ignoramos erro se já existir)
        usuario = {"username": "testuser_pytest", "password": "123"}
        await ac.post("/api/v1/auth/signup", json=usuario)

        # Faz Login
        response = await ac.post("/api/v1/auth/login", data=usuario)
        token = response.json()["access_token"]

        return {"Authorization": f"Bearer {token}"}


# --- TESTES ---


async def test_health_check():
    """Rota pública, deve funcionar sem token"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/")
    assert response.status_code == 200


async def test_criar_abastecimento_sem_token():
    """SEGURANÇA: Deve ser barrado (401) se tentar entrar sem token"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.50,
        "volume_abastecido": 20,
        "cpf_motorista": "52998224725",
        "data_hora": "2026-01-22T10:00:00",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/abastecimentos/", json=payload)

    assert response.status_code == 401  # Unauthorized!


async def test_criar_abastecimento_sucesso(token_autenticado):
    """Deve funcionar usando o token gerado pela fixture"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "ETANOL",
        "preco_por_litro": 3.40,
        "volume_abastecido": 50,
        "cpf_motorista": "52998224725",
        "data_hora": "2026-01-22T12:00:00",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        #  AQUI ESTÁ A CHAVE: Passamos o header com o token
        response = await ac.post(
            "/api/v1/abastecimentos/", json=payload, headers=token_autenticado
        )

    assert response.status_code == 201
    assert "id" in response.json()


async def test_detectar_anomalia_preco_alto(token_autenticado):
    """Testa regra de negócio (também precisa de token)"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 100.00,
        "volume_abastecido": 50,
        "cpf_motorista": "52998224725",
        "data_hora": "2026-01-22T12:00:00",
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post(
            "/api/v1/abastecimentos/", json=payload, headers=token_autenticado
        )

    assert response.status_code == 201
    assert response.json()["improper_data"] is True
