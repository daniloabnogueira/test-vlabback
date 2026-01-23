# 🚛 V-Lab Transport API & Dashboard

Sistema completo de gestão de abastecimentos com arquitetura de microsserviços, detecção de anomalias em tempo real e dashboard interativo.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async), Pydantic.
* **Banco de Dados:** PostgreSQL 15.
* **Frontend:** Streamlit, Pandas, Plotly.
* **Infraestrutura:** Docker, Docker Compose (Multi-stage builds).
* **Qualidade:** Black, Isort, Ruff.
* **Testes:** Pytest, Faker.

## ⚙️ Arquitetura do Projeto

* **API (Porta 8000):** Gerencia regras de negócio, autenticação JWT e validações.
* **Frontend (Porta 3782):** Dashboard para visualização de KPIs e anomalias.
* **Load Tester:** Container "robô" que gera dados sintéticos a cada 30s para simular uso real.
* **Postgres:** Persistência dos dados.

## 🛠️ Como Rodar o Projeto

1.  **Clone o repositório:**
    ```bash
    git clone <seu-repo-url>
    cd <pasta-do-projeto>
    ```

2.  **Suba o ambiente (Docker):**
    ```bash
    docker-compose up -d --build
    ```
    *Isso iniciará a API, aplicará as migrações (Alembic) e iniciará o Frontend e o Robô de Carga automaticamente.*

3.  **Acesse os Serviços:**
    * 📄 **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * 📊 **Dashboard Interativo:** [http://localhost:3782](http://localhost:3782)

## 🤖 Controle do Robô (Load Tester)

O sistema inclui um serviço chamado `load_tester` que insere 50 novos registros a cada 30 segundos. Você pode controlar esse robô sem desligar o resto do site:

* **⏸️ Para PAUSAR a geração de dados:**
    ```bash
    docker-compose stop load_tester
    ```
    *(O gráfico para de se mexer, ideal para analisar dados com calma).*

* **▶️ Para CONTINUAR a geração de dados:**
    ```bash
    docker-compose start load_tester
    ```

* **Forçar uma carga manual extra:**
    ```bash
    docker-compose exec load_tester python load_data.py
    ```

## 🧪 Qualidade de Código e Testes

Para garantir a robustez e padronização do código, utilize os comandos abaixo:

### 1. Rodar Testes Unitários (Pytest)
Executa a bateria de testes automatizados para validar a API:
```bash
docker-compose exec api pytest
```
### 2. Verificar e Corrigir Formatação (Linters)
# Formatação automática (Black e Isort)
```bash
docker-compose exec api black .
docker-compose exec api isort .
```
```bash
# Verificação de erros lógicos (Ruff)
docker-compose exec api ruff check .
```

