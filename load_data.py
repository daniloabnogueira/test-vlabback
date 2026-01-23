import os
import random
import time

import requests
from faker import Faker

# Configurações
API_BASE = os.getenv("API_URL", "http://localhost:8000/api/v1")
API_URL = f"{API_BASE}/abastecimentos/"
AUTH_URL = f"{API_BASE}/auth"
QTD_REQUISICOES = 50
INTERVALO_ENTRE_REQUISICOES = 0.5  # Intervalo fixo ou random, como preferir

fake = Faker("pt_BR")
TIPOS_COMBUSTIVEL = ["GASOLINA", "ETANOL", "DIESEL"]


def gerar_cpf_valido():
    return fake.cpf().replace(".", "").replace("-", "")


def get_auth_token():
    """Realiza login para obter o token JWT necessário"""
    user_data = {"username": "loadtester", "password": "123"}

    # 1. Tenta criar o usuário (ignora erro se já existir)
    try:
        requests.post(f"{AUTH_URL}/signup", json=user_data)
    except Exception:
        pass

    # 2. Faz login
    print("🔑 Autenticando usuário de teste...")
    resp = requests.post(f"{AUTH_URL}/login", data=user_data)

    if resp.status_code != 200:
        print(f"❌ Falha fatal no login: {resp.text}")
        return None

    return resp.json()["access_token"]


def gerar_abastecimento_fake():
    data_fake = fake.date_time_between(start_date="-7d", end_date="now")
    combustivel = random.choice(TIPOS_COMBUSTIVEL)

    # --- SUA LÓGICA ORIGINAL DE ANOMALIA ---
    preco_base = random.uniform(3.50, 6.50)

    # 10% de chance de gerar preço anômalo (8.00 a 10.00)
    if random.random() < 0.1:
        preco_base = random.uniform(8.00, 10.00)
    # ---------------------------------------

    cpf_limpo = gerar_cpf_valido()

    return {
        "id_posto": random.randint(1, 10),
        "tipo_combustivel": combustivel,
        "preco_por_litro": round(preco_base, 2),
        "volume_abastecido": round(random.uniform(10.0, 80.0), 2),
        "cpf_motorista": cpf_limpo,
        "data_hora": data_fake.isoformat(),
    }


def executar_teste_carga():
    # 1. Obter Token
    token = get_auth_token()
    if not token:
        return

    # No requests, o header de autorização é passado assim:
    headers = {"Authorization": f"Bearer {token}"}

    print("🚀 Iniciando Teste de Carga (Requests + Auth)")
    print(f"🎯 Meta: {QTD_REQUISICOES} requisições")

    sucessos = 0
    erros = 0
    anomalias = 0
    start_time = time.time()

    for i in range(1, QTD_REQUISICOES + 1):
        payload = gerar_abastecimento_fake()

        try:
            # Envio usando requests com o cabeçalho de autorização
            response = requests.post(API_URL, json=payload, headers=headers)

            if response.status_code == 201:
                dados = response.json()

                # Verifica visualmente se a API detectou a anomalia
                if dados.get("improper_data"):
                    status = "🚨 ANOMALIA DETECTADA"
                    anomalias += 1
                else:
                    status = "✅ OK"

                print(
                    f"#{i} [ID {dados['id']}] {payload['tipo_combustivel']} R$ {payload['preco_por_litro']} - {status}"
                )
                sucessos += 1
            else:
                print(f"#{i} ❌ Erro {response.status_code}: {response.text}")
                erros += 1

        except Exception as e:
            print(f"⚠️ Erro de conexão: {e}")
            erros += 1

        time.sleep(INTERVALO_ENTRE_REQUISICOES)

    print("\n" + "=" * 40)
    print(f"🏁 FIM DO TESTE em {time.time() - start_time:.2f}s")
    print(f"✅ Sucessos: {sucessos}")
    print(f"🚨 Anomalias Geradas/Detectadas: {anomalias}")
    print(f"❌ Falhas: {erros}")
    print("=" * 40)


if __name__ == "__main__":
    executar_teste_carga()
