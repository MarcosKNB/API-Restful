from decimal import Decimal
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional
from enum import Enum

import re


class TipoUsuario(str, Enum):
    produtor = "produtor"
    comprador = "comprador"
    admin = "admin"


class TipoProduto(str, Enum):
    frutas = "frutas"
    graos = "graos"
    laticinios = "laticinios"


class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=3)
    email: EmailStr
    tipo: TipoUsuario
    localizacao: Optional[str] = Field(None, max_length=100)

    class Config:
        from_attributes = True


class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=8)

    @field_validator("senha")
    def validarSenha(cls, value):
        if not re.search(r"[a-zA-Z]", value):
            raise ValueError("senha deve conter pelo menos uma letra")
        if not re.search(r"[\d]", value):
            raise ValueError("senha deve conter pelo menbos um numero")
        return value


class UsuarioResponse(UsuarioBase):
    id: int

    class Config:
        from_attributes = True


class Produto(BaseModel):
    nome: str = Field(..., min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Decimal = Field(..., max_digits=10, decimal_places=2, gt=Decimal("0.00"))
    quantidade: int = Field(..., ge=0)
    categoria: TipoProduto
    localizacao: Optional[str] = Field(None)

    class Config:
        from_attributes = True


class ProdutoCreate(Produto):
    pass


class ProdutoResponse(Produto):
    id: int
    produtor_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=3, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: Optional[Decimal] = Field(
        None, max_digits=10, decimal_places=2, gt=Decimal("0.00")
    )
    quantidade: Optional[int] = Field(None, ge=0)
    categoria: Optional[TipoProduto] = None
    localizacao: Optional[str] = Field(None)

    class Config:
        from_attributes = True
