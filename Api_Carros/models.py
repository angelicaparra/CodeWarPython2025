from sqlalchemy import Column, Integer, String, Text

from fast_car_api.database import Base


class Car(Base):
    __tablename__ = 'cars'

    id = Column(Integer, primary_key=True, index=True)
    modelo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    marca = Column(String, nullable=True)
    ano = Column(Integer, nullable=True)
    cor = Column(String, nullable=True)
    tipo_combustivel = Column(String, nullable=True)
    modificacao = Column(Text, nullable=True)
