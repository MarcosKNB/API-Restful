import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from dotenv import load_dotenv

load_dotenv()

metadata_obj = MetaData()


class Base(DeclarativeBase):
    metadata = metadata_obj


DATABASE_URL = os.getenv("DATABASE_URL")


if not DATABASE_URL:
    raise EnvironmentError(
        "ERRO: DATABASE_URL não foi definida.Crie um arquivo .env na raiz do projeto."
    )

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
