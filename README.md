API Marketplace Agro

Uma API RESTful robusta, construída com FastAPI e SQLAlchemy, para gerenciar um marketplace agrícola. A aplicação permite o cadastro de usuários com diferentes papéis (produtor, comprador, admin) e o gerenciamento de produtos, com um sistema de autenticação seguro baseado em JWT.

🚀 Funcionalidades Principais

    Autenticação de Usuários: Sistema de login completo com tokens de acesso JWT (OAuth2).

    Autorização por Papel (Roles):

        Admins: Podem listar e deletar qualquer usuário.

        Produtores: Podem criar, ler, atualizar e deletar seus próprios produtos.

        Compradores: Podem se cadastrar e listar produtos.

    Proteção de Rotas: Endpoints seguros que só podem ser acessados pelo "dono" do recurso ou por um admin.

    Validação de Dados: Validação automática de requisições e respostas usando Pydantic.

    Pronto para Docker: Configuração completa com docker-compose.yml para rodar a API e o banco de dados em containers.

    Documentação Automática: Documentação interativa da API gerada automaticamente pelo FastAPI (Swagger UI e ReDoc).

🛠️ Tecnologias Utilizadas

Aqui estão as principais ferramentas e bibliotecas usadas neste projeto.

    Linguagem: Python 3.10+

    SGBD (Banco de Dados): MariaDB (v10.11+)

Bibliotecas Principais

Biblioteca	Versão (Exemplo)	Propósito
fastapi	~0.110.0	O framework principal da API.
uvicorn	~0.29.0	O servidor (ASGI) que executa a aplicação.
sqlalchemy	~2.0.29	O ORM (Mapeador Objeto-Relacional) para interagir com o banco.
mysql-connector-python	~8.4.0	O "driver" que permite ao SQLAlchemy se comunicar com o MariaDB/MySQL.
passlib	~1.7.4	Para hashear e verificar senhas de forma segura (usando sha256_crypt).
python-jose[cryptography]	~3.3.0	Para criar e validar os tokens de login (JWT).
pydantic	~2.7.0	Para validação de dados, usado extensivamente nos schemas.
python-multipart	~0.0.9	Necessário para o FastAPI ler dados de formulário (usado no login OAuth2).
email-validator	~2.1.1	Usado pelo Pydantic para validar o tipo EmailStr.
