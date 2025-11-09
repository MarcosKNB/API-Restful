from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from . import crud, models, schemas, security
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---Dependencias para execucao---


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """Verifica usuario logado"""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais não validadas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, security.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception

    # token_data.email já foi validado como não-None acima
    usuario = crud.get_usuario_por_email(db, email=email)
    if usuario is None:
        raise credentials_exception
    # Garantir que o atributo 'tipo' seja uma instância de Enum Python (TipoUsuario)
    # Alguns backends/versões do SQLAlchemy podem devolver o valor cru; normalizamos aqui
    try:
        usuario.tipo = schemas.TipoUsuario(usuario.tipo)
    except Exception:
        # se já for o Enum ou valor inválido, mantemos como está
        pass
    return usuario


async def get_user_admin(current_user: models.Usuario = Depends(get_current_user)):
    """Verifica se o usuario 'e admin"""
    if current_user.tipo != models.TipoUsuario.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso restrito a administradores",
        )
    return current_user


async def get_produto_e_verificar_dono(
    produto_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
) -> models.Produto:
    """Verifica se o produto existe e se o produto pertence ao usuario logado"""

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
