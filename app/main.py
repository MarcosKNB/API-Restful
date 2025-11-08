from fastapi import FastAPI
from .database import engine, metadata_obj
from .rotas import autenticacao, usuarios, produtos

# Cria as tabelas no banco de dados
metadata_obj.create_all(bind=engine)
app = FastAPI

# --- Criação da Aplicação ---
app = FastAPI(
    title="API Marketplace Agro",
    description="API para gerenciar usuários (produtores/compradores/administradores) e produtos agrícolas.",
    version="1.0.0",
)

# --- Configuração de Autenticação ---

app.include_router(autenticacao.router)
app.include_router(usuarios.router)
app.include_router(produtos.router)


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "API Marketplace Agro está funcionando!"}
