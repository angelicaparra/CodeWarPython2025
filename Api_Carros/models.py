from sqlalchemy import Column, Integer, String

from Api_Carros.database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=True)
    modelo = Column(String, nullable=False)
    cor = Column(String, nullable=True)
    ano = Column(Integer, nullable=True)
    tipo_combustivel = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
