from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from .. import crud, schemas, security
from ..deps import get_db

router = APIRouter(tags=["Autenticacao"])


@router.post("/token", response_model=schemas.Token, tags=["Autenticacao"])
async def login_para_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """Login - Gera um token de acesso"""

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
