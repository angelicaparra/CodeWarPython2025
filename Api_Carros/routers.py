from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from Api_Carros.database import get_session
from Api_Carros.models import Car
from Api_Carros.schemas import (
    CarList,
    CarPublic,
    CarSchema,
)

router = APIRouter(
    prefix='/api/v1/carros',
    tags=['carros'],
)

#iniciando o Crud [INSERT]
@router.post(
        path='/', 
        response_model=CarPublic, 
        status_code=status.HTTP_201_CREATED, #Retorno de Criacao
)
def create_car(car: CarSchema,session: Session = Depends(get_session)): #incluindo dependencia do banco
    car = Car(**car.model_dump())
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

# CRUD [LISTAR]
@router.get(
    path='/',
    response_model=CarList,
    status_code=status.HTTP_200_OK,
)
def list_cars(session : Session = Depends(get_session)):
    query = session.scalars(select(Car))
    cars = query.all()
    return {'cars': cars}
