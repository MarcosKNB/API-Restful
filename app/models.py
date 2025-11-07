from sqlalchemy import Column, Integer, String, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from .schemas import TipoUsuario, TipoProduto


class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuario), nullable=False)
    localizacao = Column(String(100), nullable=True)

    produtos = relationship("Produto", back_populates="produtor")


class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(String(500), nullable=True)
    preco = Column(DECIMAL(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    categoria = Column(Enum(TipoProduto), nullable=False)
    localizacao = Column(String(255), nullable=True)
    produtor_id = Column(Integer, ForeignKey("usuarios.id"))

    produtor = relationship("Usuario", back_populates="produtos")
