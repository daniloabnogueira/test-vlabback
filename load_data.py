import requests
import random 
import time
from faker import Faker
from datetime import datetime, timedelta

API_URL = 'http://localhost:8000/api/v1/abastecimentos/'
QTD_REQUISICOES = 50
INTERVALO_ENTRE_REQUISICOES = 0.05

fake = Faker('pt_BR')
TIPOS_COMBUSTIVEL = ["GASOLINA", "ETANOL", "DIESEL"]

def gerar_abastecimento_fake():
    data_fake = fake.date_time_between(start_date='-7d', end_date='now')
    combustivel = random.choice(TIPOS_COMBUSTIVEL)

    preco_base = random.uniform(3.50, 6.50)
    if random.random() < 0.1:
        preco_base = random.uniform(8.00, 10.00)
    
    cpf_limpo = fake.cpf().replace('.', '').replace('-', '')

    return {
        "id_posto": random.randint(1, 10),
        "tipo_combustivel": combustivel,
        "preco_por_litro": round(preco_base, 2),
        "volume_abastecido": round(random.uniform(10.0, 80.0), 2),
        "cpf_motorista": cpf_limpo,
        "data_hora": data_fake.isoformat()
    }

def executar_teste_carga():
    print(f"Iniciando Teste de Stress (Faker) via Docker")
    print(f"Meta: {QTD_REQUISICOES} requisições")

    sucessos = 0
    erros = 0
    start_time = time.time()

    for i in range(1, QTD_REQUISICOES + 1):
        payload = gerar_abastecimento_fake()
        try:
            response = requests.post(API_URL, json=payload)
            if response.status_code == 201:
                dados = response.json()
                status = "ANOMALIA" if dados['improper_data'] else "OK"
                print(f"#{i} [ID{dados['id']}] {payload['tipo_combustivel']} - {status}")
                sucessos += 1
            else:
                print(f"#{i} Erro {response.status_code}: {response.text}")
                erros += 1
        except Exception as e:
            print(f"Erro: {e}")
            erros += 1
        time.sleep(INTERVALO_ENTRE_REQUISICOES)
    
    print(f"\n FIM. Total: {time.time() - start_time:.2f}s | Sucessos: {sucessos} | Falhas: {erros}")

if __name__ == "__main__":
    executar_teste_carga()