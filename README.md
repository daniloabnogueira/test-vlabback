# test-vlabback

# 🚛 V-Lab Transport API & Dashboard

Sistema completo de gestão de abastecimentos com arquitetura de microsserviços, detecção de anomalias em tempo real e dashboard interativo.

## 🚀 Tecnologias Utilizadas

* **Backend:** Python 3.11, FastAPI, SQLAlchemy (Async), Pydantic.
* **Banco de Dados:** PostgreSQL 15.
* **Frontend:** Streamlit, Pandas, Plotly.
* **Infraestrutura:** Docker, Docker Compose (Multi-stage builds).
* **Qualidade:** Black, Isort, Ruff.
* **Testes:** Pytest.

## ⚙️ Arquitetura do Projeto

* **API (Porta 8000):** Gerencia regras de negócio, autenticação JWT e validações.
* **Frontend (Porta 3782):** Dashboard para visualização de KPIs e anomalias.
* **Load Tester:** Robô autônomo que gera dados sintéticos a cada 30s para teste de carga.
* **Postgres:** Persistência dos dados.

## 🛠️ Como Rodar

1.  **Clone o repositório:**
    ```bash
    git clone <seu-repo-url>
    cd <pasta-do-projeto>
    ```

2.  **Suba o ambiente (Docker):**
    ```bash
    docker-compose up -d --build
    ```
    *Isso iniciará a API, aplicará as migrações (Alembic) e iniciará o Frontend e o Robô de Carga.*

3.  **Acesse os Serviços:**
    * 📄 **Documentação da API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
    * 📊 **Dashboard:** [http://localhost:3782](http://localhost:3782)

## 🧪 Teste de Stress (Carga de Dados)

O projeto inclui um script para popular o banco de dados e testar a performance da API.

Para executar, não é necessário instalar nada localmente. Basta rodar o comando abaixo após subir os containers:

```bash
docker-compose exec api python load_data.py

## 🧪 Testes e Qualidade

Para rodar a formatação e verificações de qualidade:

```bash
docker-compose exec api black .
docker-compose exec api ruff check .