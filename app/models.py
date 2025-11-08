from sqlalchemy import Integer, String, DECIMAL, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from .schemas import TipoUsuario, TipoProduto
from decimal import Decimal

# ---Modelos para o banco de dados---


class Usuario(Base):
    __tablename__: str = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    tipo: Mapped[TipoUsuario] = mapped_column(Enum(TipoUsuario), nullable=False)
    localizacao: Mapped[str | None] = mapped_column(String(100), nullable=True)

    produtos: Mapped[list["Produto"]] = relationship(back_populates="produtor")


class Produto(Base):
    __tablename__: str = "produtos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    descricao: Mapped[str | None] = mapped_column(String(500), nullable=True)

    preco: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    categoria: Mapped[TipoProduto] = mapped_column(Enum(TipoProduto), nullable=False)
    localizacao: Mapped[str | None] = mapped_column(String(255), nullable=True)

    produtor_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"))

    produtor: Mapped["Usuario"] = relationship(back_populates="produtos")
