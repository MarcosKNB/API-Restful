from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator
from enum import Enum
import re

# --- Enums ---


class TipoUsuario(str, Enum):
    produtor = "produtor"
    comprador = "comprador"
    admin = "admin"


class TipoProduto(str, Enum):
    frutas = "frutas"
    graos = "graos"
    laticinios = "laticinios"


# --- Schemas de Usuario ---


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3)
    email: EmailStr
    tipo: TipoUsuario
    localizacao: str | None = Field(None, max_length=100)

    class Config:
        from_attributes: bool = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)

    @field_validator("senha")
    def validarSenha(cls, value: str) -> str:
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("senha deve conter pelo menos uma letra")
        if not re.search(r"[\d]", value):
            raise ValueError("senha deve conter pelo menbos um numero")
        return value


class UsuarioResponse(UsuarioBase):
    id: int


# --- Schemas de Produto ---


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: str | None = Field(None, max_length=500)
    preco: Decimal = Field(..., max_digits=10, decimal_places=2, gt=Decimal("0.00"))
    quantidade: int = Field(..., ge=0)
    categoria: TipoProduto
    localizacao: str | None = Field(None)

    class Config:
        from_attributes: bool = True


class ProdutoUpdate(BaseModel):
    nome: str | None = Field(None, min_length=3, max_length=100)
    descricao: str | None = Field(None, max_length=500)
    preco: Decimal | None = Field(
        None, max_digits=10, decimal_places=2, gt=Decimal("0.00")
    )
    quantidade: int | None = Field(None, ge=0)
    categoria: TipoProduto | None = None
    localizacao: str | None = Field(None)

    class Config:
        from_attributes: bool = True


class ProdutoCreate(ProdutoBase):
    produtor_id: int = Field(...)


class ProdutoResponse(ProdutoBase):
    id: int
    produtor_id: int


# --- Schemas de Autenticacao ---


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
