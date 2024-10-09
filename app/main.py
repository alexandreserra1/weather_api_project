# app/main.py

from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(
    title="API de Dados Climáticos",
    description="Uma API para consultar dados climáticos armazenados.",
    version="1.0.0"
)

app.include_router(endpoints.router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Bem-vindo à API de Dados Climáticos!"}
