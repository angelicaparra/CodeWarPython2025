from fastapi import FastAPI

from Api_Carros.routers import router as carros_rota

app = FastAPI(
    title='API de Carros – Gerenciamento de Frotas Inteligente',
    description='CodeWar Python + Análise de Dados 2025',
    version='0.1.0',
)

app.include_router(carros_rota)

#Declarando minha primeira rota
@app.get('/')
def read_root():
    return {'status': 'ok'}