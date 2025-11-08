from fastapi import FastAPI
from .database import engine, metadata_obj
from .rotas import autenticacao, usuarios, produtos

# Cria as tabelas no banco de dados
metadata_obj.create_all(bind=engine)

# --- Criacao da Aplicacao ---
app = FastAPI(
    title="API Marketplace Agro",
    description="API para gerenciar usuarios produtos agricolas",
)

# --- Configuracao de rotas ---

app.include_router(autenticacao.router)
app.include_router(usuarios.router)
app.include_router(produtos.router)


# Verificar se esta no ar
@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "API Marketplace Agro esta funcionando!"}
