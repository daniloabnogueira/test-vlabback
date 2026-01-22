import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

BASE_URL = "http://test"

#@pytest.mark.asyncio
async def test_health_check():
    """Testa de a rota raiz (Health Check) responde 200 OK"""
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API rodando com sucesso!"}

#@pytest.mark.asyncio
async def test_criar_abastecimento_cpf_invalido():
    """Testa se a API rejeita um CPF com digitos verificadores errados"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 5.50,
        "volume_abastecido": 20,
        "cpf_motorista": "11122233300", # CPF inválido de propósito
        "data_hora": "2026-01-22T10:00:00"
    }
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/abastecimentos/", json=payload)
    
    #Espero erro 422 
    assert response.status_code == 422
    #Verfica se a mensagem de erro menciona o CPF
    assert "CPF inválido" in response.text

#@pytest.mark.asyncio
async def test_criar_abastecimento_sucesso():
    """Testa o fluxo feliz: Criar um abastecimento válido"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "ETANOL",
        "preco_por_litro": 3.40,
        "volume_abastecido": 50,
        "cpf_motorista": "52998224725", # CPF Válido
        "data_hora": "2026-01-22T12:00:00"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/abastecimentos/", json=payload)
    
    assert response.status_code == 201
    dados = response.json()
    assert dados["cpf_motorista"] == payload["cpf_motorista"]
    assert "id" in dados

#@pytest.mark.asyncio
async def test_detectar_anomalia_preco_alto():
    """Testa se a Regra de Negócio marca como anomalia (improper_data) um preço absurdo"""
    payload = {
        "id_posto": 1,
        "tipo_combustivel": "GASOLINA",
        "preco_por_litro": 100.00,  # Preço absurdo para ativar a regra
        "volume_abastecido": 50,
        "cpf_motorista": "52998224725", # CPF Válido
        "data_hora": "2026-01-22T12:00:00"
    }
    
    async with AsyncClient(transport=ASGITransport(app=app), base_url=BASE_URL) as ac:
        response = await ac.post("/api/v1/abastecimentos/", json=payload)
    
    assert response.status_code == 201
    
    # AQUI É O TESTE DA REGRA DE NEGÓCIO:
    # O campo improper_data TEM que ser True
    assert response.json()["improper_data"] is True