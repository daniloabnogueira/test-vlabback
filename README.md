# test-vlabback

## 🧪 Teste de Stress (Carga de Dados)

O projeto inclui um script para popular o banco de dados e testar a performance da API.

Para executar, não é necessário instalar nada localmente. Basta rodar o comando abaixo após subir os containers:

```bash
docker-compose exec api python load_data.py