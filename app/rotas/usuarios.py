from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..deps import get_db, get_current_user, get_user_admin

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post(
    "/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuarios"],
)
def create_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Cria um novo usuário."""

    db_usuario = crud.get_usuario_por_email(db, email=usuario.email)
    if db_usuario:
        raise HTTPException(status_code=400, detail="Email já registrado")
    return crud.create_usuario(db=db, usuario=usuario)


@router.get("/me", response_model=schemas.UsuarioResponse, tags=["Usuarios"])
async def read_users_me(current_user: models.Usuario = Depends(get_current_user)):
    """Retorna os dados do usuário logado."""
    return current_user


@router.get(
    "/",
    response_model=List[schemas.UsuarioResponse],
    tags=["Usuarios - Admin"],
)
def read_usuarios(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    admin: models.Usuario = Depends(get_user_admin),
):
    """(Admin) Retorna uma lista de todos os usuários."""
    usuarios = crud.get_usuarios(db, skip=skip, limit=limit)
    return usuarios


@router.delete(
    "/{usuario_id}",
    response_model=schemas.UsuarioResponse,
    tags=["Usuarios - Admin"],
)
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    admin: models.Usuario = Depends(get_user_admin),
):
    if usuario_id == admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nao pode excluir a si mesmo",
        )

    usuario = crud.delete_usuario(db, usuario_id=usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario nao encontrado na base de dados",
        )

    return usuario
