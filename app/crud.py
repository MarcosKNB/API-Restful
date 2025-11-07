from sqlalchemy.orm import Session
from .security import get_hash_senha

from . import models, schemas


def get_usuario(db: Session, usuario_id: int):
    return db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()


def create_usuario(db: Session, usuario: schemas.UsuarioCreate):
    senha_hasheada = get_hash_senha(usuario.senha)

    db_usuario = models.Usuario(
        nome=usuario.nome,
        email=usuario.email,
        senha=senha_hasheada,
        tipo=usuario.tipo,
        localizacao=usuario.localizacao,
    )

    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario


def get_usuarios(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Usuario).offset(skip).limit(limit).all()


def get_usuario_por_email(db: Session, email: str):
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def get_produto(db: Session, produto_id: int):
    return db.query(models.Produto).filter(models.Produto.id == produto_id).first()


def get_produtos(db: Session, skip: int = 0, limit: int = 50):
    return db.query(models.Produto).offset(skip).limit(limit).all()


def get_produtos_por_produtor(db: Session, produtor_id: int):
    return (
        db.query(models.Produto).filter(models.Produto.produtor_id == produtor_id).all()
    )


def create_produto(db: Session, produto: schemas.ProdutoCreate, produtor_id: int):
    db_produto = models.Produto(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade=produto.quantidade,
        categoria=produto.categoria,
        localizacao=produto.localizacao,
        produtor_id=produtor_id,
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto


def update_produto(
    db: Session, produto: models.Produto, produto_update: schemas.ProdutoUpdate
):
    update_data = produto_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(produto, key, value)

    db.add(produto)
    db.commit()
    db.refresh(produto)
    return produto


def delete_produto(db: Session, produto: models.Produto):
    db.delete(produto)
    db.commit()
    return produto
