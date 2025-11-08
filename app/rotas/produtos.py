from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..deps import get_db, get_current_user, get_produto_e_verificar_dono

router = APIRouter(prefix="/produtos")


@router.post(
    "/",
    response_model=schemas.ProdutoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Produtos - Gerenciamento"],
)
def create_produto(
    produto: schemas.ProdutoCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    """Produtor - Cria um novo produto"""
    if current_user.tipo != schemas.TipoUsuario.produtor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Apenas produtor cria produto"
        )

    return crud.create_produto(db=db, produto=produto, produtor_id=current_user.id)


@router.get(
    "/",
    response_model=List[schemas.ProdutoResponse],
    tags=["Produtos - Publico"],
)
def read_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Publico - Retorna uma lista de todos os produtos"""
    produtos = crud.get_produtos(db, skip=skip, limit=limit)
    return produtos


@router.get(
    "/me",
    response_model=List[schemas.ProdutoResponse],
    tags=["Produtos - Gerenciamento"],
)
async def ver_meus_produtos(
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retorna a lista de produtos do produtor logado"""

    if current_user.tipo != schemas.TipoUsuario.produtor:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Apenas produtores podem ver 'meus produtos'",
        )

    return crud.get_produtos_por_produtor(db, produtor_id=current_user.id)


@router.get(
    "/{id}", response_model=schemas.ProdutoResponse, tags=["Produtos - Publico(Logado)"]
)
async def ver_produto_por_id(
    produto_id: int,
    current_user: models.Usuario = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Qualquer logado - Visualizar produto especifico do id"""
    produto = crud.get_produto(db, produto_id=produto_id)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado na base de dados",
        )
    return produto


@router.put(
    "/{produto_id}",
    response_model=schemas.ProdutoResponse,
    tags=["Produtos - Gerenciamento"],
)
async def update_meu_produto(
    produto_id: int,
    produto_update: schemas.ProdutoUpdate,
    db_produto: models.Produto = Depends(get_produto_e_verificar_dono),
    db: Session = Depends(get_db),
):
    """Atualiza um produto do produtor logado pelo id"""

    return crud.update_produto(db=db, produto=db_produto, produto_update=produto_update)


@router.delete(
    "/{produto_id}",
    response_model=schemas.ProdutoResponse,
    tags=["Produtos - Gerenciamento"],
)
async def delete_meu_produto(
    produto_id: int,
    db_produto: models.Produto = Depends(get_produto_e_verificar_dono),
    db: Session = Depends(get_db),
):
    """Deleta um produto do produtor logado pelo id"""

    return crud.delete_produto(db=db, produto=db_produto)
