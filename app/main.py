from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from jose import JWTError, jwt
from datetime import timedelta


from . import crud, models, schemas, security
from .database import SessionLocal, engine

# Cria as tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

# --- Criação da Aplicação ---
app = FastAPI(
    title="API Marketplace Agro",
    description="API para gerenciar usuários (produtores/compradores/administradores) e produtos agrícolas.",
    version="1.0.0",
)

# --- Configuração de Autenticação ---
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- Dependências ---


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais não validadas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    usuario = crud.get_usuario_por_email(db, email=token_data.email)
    if usuario is None:
        raise credentials_exception
    return usuario


async def get_produto_e_verificar_dono(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
) -> models.Produto:
    db_produto = crud.get_produto(db, produto_id=produto_id)

    if db_produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado"
        )

    if current_user.tipo != schemas.TipoUsuario.produtor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário logado não é produtor",
        )

    if db_produto.produtor_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Esse produto não te pertence"
        )
    return db_produto


# --- Endpoints de Autenticação e Usuários ---


@app.post("/token", response_model=schemas.Token, tags=["Autenticação"])
async def login_para_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Gera um token de acesso (login)."""

    usuario = crud.get_usuario_por_email(db, email=form_data.username)

    if not usuario or not security.verificar_senha(form_data.password, usuario.senha):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": usuario.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@app.post(
    "/usuarios/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuários"],
)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""

    db_usuario = crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_usuario(db=db, usuario=usuario)


@app.get("/usuarios/me", response_model=schemas.UsuarioResponse, tags=["Usuários"])
async def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    """Retorna os dados do usuário logado."""
    return current_user


@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse], tags=["Usuários"])
def read_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """(Admin) Retorna uma lista de todos os usuários."""
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


# --- Endpoints para Produtos ---


@app.post(
    "/produtos/",
    response_model=schemas.ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos (Gerenciamento)"],
)
def create_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    """Cria um novo produto (apenas para produtores)."""
    if current_user.tipo != schemas.TipoUsuario.produtor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Apenas produtor cria produto"
        )

    return crud.create_produto(db=db, produto=produto, produtor_id=current_user.id)


@app.get(
    "/produtos/",
    response_model=List[schemas.ProdutoResponse],
    tags=["Produtos (Público)"],
)
def read_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retorna uma lista de todos os produtos (público)."""
    produtos = crud.get_produtos(db, skip=skip, limit=limit)
    return produtos


@app.get(
    "/produtos/me",
    response_model=List[schemas.ProdutoResponse],
    tags=["Produtos (Gerenciamento)"],
)
async def ver_meus_produtos(
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retorna a lista de produtos do produtor logado."""

    if current_user.tipo != schemas.TipoUsuario.produtor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas produtores podem ver 'meus produtos'",
        )

    return crud.get_produtos_por_produtor(db, produtor_id=current_user.id)


@app.put(
    "/produtos/{produto_id}",
    response_model=schemas.ProdutoResponse,
    tags=["Produtos (Gerenciamento)"],
)
async def update_meu_produto(
    produto_id: int,
    produto_update: schemas.ProdutoUpdate,
    db_produto: models.Produto = Depends(get_produto_e_verificar_dono),
    db: Session = Depends(get_db),
):
    """Atualiza um produto do produtor logado."""

    return crud.update_produto(db=db, produto=db_produto, produto_update=produto_update)


@app.delete(
    "/produtos/{produto_id}",
    response_model=schemas.ProdutoResponse,
    tags=["Produtos (Gerenciamento)"],
)
async def delete_meu_produto(
    produto_id: int,
    db_produto: models.Produto = Depends(get_produto_e_verificar_dono),
    db: Session = Depends(get_db),
):
    """Deleta um produto do produtor logado."""

    return crud.delete_produto(db=db, produto=db_produto)


@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "API Marketplace Agro está funcionando!"}
