from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Transporte API")

app.include_router(router)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}