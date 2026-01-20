from fastapi import FastAPI

app = FastAPI(title="Transporte API")

@app.get("/")
def read_root():
    return {"message": "Ambiente Docker configurado com sucesso!"}