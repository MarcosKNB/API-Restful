# API Marketplace Agro

Projeto simples em FastAPI para gerenciar usuários e produtos agrícolas (produtores e compradores).

## Visão geral

- Framework: FastAPI
- Banco: SQLAlchemy (configurado em `app/database.py`)
- Autenticação: JWT (rota `/token` produz `access_token`)

O projeto fornece rotas para autenticação, gerenciamento de usuários e produtos.

## Dependências

As dependências estão em `requirements.txt`. Principais pacotes:

- fastapi
- uvicorn[standard]
- sqlalchemy
- mysql-connector-python
- passlib
- python-jose[cryptography]
- email-validator
- python-multipart

Instalar dependências:

```bash
python3 -m pip install -r requirements.txt
```

## Como rodar (desenvolvimento)

Rodar a API com uvicorn:

```bash
uvicorn "app.main:app" --reload --host 0.0.0.0 --port 8000
```

Depois disso a API estará disponível em `http://127.0.0.1:8000`.

Endpoints úteis:

- Health check: `GET /` — retorna mensagem de funcionamento.
- Token (login): `POST /token` — usa `OAuth2PasswordRequestForm` (fields: username=email, password) e retorna JSON com `access_token` e `token_type`.

As rotas cadastradas no projeto estão em `app/rotas/`:

- `autenticacao.py` — rota `/token` para autenticação (gera JWT)
- `usuarios.py` — rotas relacionadas a usuários
- `produtos.py` — rotas relacionadas a produtos

## Observações / notas técnicas

- Em `app/models.py` os tipos `TipoUsuario` e `TipoProduto` são armazenados como Enum (p.ex. `"produtor"`, `"comprador"`).
- A função de autenticação retorna um dicionário com `access_token` e `token_type` (ex: `{"access_token": "...", "token_type": "bearer"}`) — isso já está compatível com o `OAuth2PasswordBearer` usado pelo FastAPI.
- Em `app/main.py` há uma linha redundante `app = FastAPI` (sem parênteses) antes da criação correta da instância `app = FastAPI(...)`. Isso não causa erro porque em seguida a variável é sobrescrita, mas é aconselhável remover a linha redundante para manter o código limpo:

```py
# Remover ou alterar:
app = FastAPI

# Manter:
app = FastAPI(
    title="API Marketplace Agro",
    description="API para gerenciar usuarios produtos agricolas",
)
```

- Se você estiver enfrentando o erro "Invalid conditional operand of type \"ColumnElement[bool]\"" isso normalmente significa que em algum ponto do código você está tentando usar uma expressão SQLAlchemy (por exemplo, `some_column == value`) diretamente numa condição Python (`if <sql expression>:`). A correção é garantir que a dependência que retorna o usuário autenticado (`get_current_user` / `getCurrentUser`) devolva uma instância ORM (atributos já resolvidos em valores Python) e que comparações com `Enum` usem o membro correto ou `.value` quando necessário. Posso ajudar a corrigir esse ponto se você me enviar o arquivo que implementa a dependência de autenticação (provavelmente `app/security.py` ou `app/deps.py`).

## Próximos passos sugeridos

1. Remover a linha redundante em `app/main.py` para limpar o código.
2. Se o erro de `ColumnElement[bool]` persistir, envie o arquivo que implementa a dependência de usuário atual (por exemplo, `app/deps.py` ou `app/security.py`) e eu corrijo a lógica.

---

Se quiser, eu já aplico a remoção da linha redundante em `app/main.py` e/ou corrijo a dependência que produz o `ColumnElement[bool]` — diga qual opção prefere.