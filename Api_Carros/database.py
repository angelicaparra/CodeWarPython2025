from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///cars.db'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#Função para chama a sessão
def get_session():
    session = SessionLocal() #cria uma conexão com banco
    try:
        yield session #é ativado durante o uso da sessão
    finally:
        session.close()