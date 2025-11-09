import sys
from dotenv import load_dotenv
from sqlalchemy.exc import OperationalError, ProgrammingError

load_dotenv()
"""Arquivo para criacao de um usuario admin para testes"""
sys.path.append("app")

try:
    from app.database import SessionLocal
    from app.schemas import UsuarioCreate, TipoUsuario
    from app import crud

except ImportError as e:
    print(f"Erro de importacao: {e}")
    print("Verifica se a pasta app existe e a cofiguracao do .env")
    sys.exit(1)


def create_admin_user():
    """Cria um usuário de teste (admin) no banco de dados."""

    # --- Defina seu usuario de teste aqui ---
    ADMIN_EMAIL = "admin@email.com"
    ADMIN_PASSWORD = "AdminSenha123"
    ADMIN_NOME = "Administrador"

    # Criar uma sessao de banco
    try:
        db = SessionLocal()
    except Exception as e:
        print(f"Nao foi possivel conectar ao banco: {e}")
        print("Verifique se banco local ou docker ta rodando e se a .env ta certa")
        return

    # Preparar os dados do usuario
    try:
        test_user = UsuarioCreate(
            nome=ADMIN_NOME,
            email=ADMIN_EMAIL,
            senha=ADMIN_PASSWORD,
            tipo=TipoUsuario.admin,
            localizacao="Sistema",
        )
    except Exception as e:
        print(f"Erro ao validar dados do schema: {e}")
        db.close()
        return

    try:
        db_user = crud.get_usuario_por_email(db, email=test_user.email)

        if db_user:
            print(f"Erro, usuario '{ADMIN_EMAIL}' ja existe")
        else:
            crud.create_usuario(db=db, usuario=test_user)
            print(f"Usuario '{ADMIN_EMAIL}' criado")

    except (OperationalError, ProgrammingError) as e:
        print(f"Erro no Banco de Dados: {e}")
        print("Verifique se as tabelas foram criadas, tente rodar o Docker primeiro")
        db.rollback()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_admin_user()
