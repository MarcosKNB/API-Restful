from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://root:chavesnobre12@localhost/marketplace_agro"

metadata_obj = MetaData()
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    metadata = metadata_obj
