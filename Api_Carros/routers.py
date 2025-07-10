from fastapi import APIRouter, Depends, HTTPException, status
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
def list_cars(
    session : Session = Depends(get_session),
    offset: int = 0, #limitando quantidades de registro quero ver
    limit: int = 100,
):
    query = session.scalars(select(Car).offset(offset).limit(limit))
    cars = query.all()
    return {'cars': cars}
# CRUD [GET POR ID]
@router.get(
    path='/{car_id}',
    response_model=CarPublic,
    status_code=status.HTTP_200_OK,
)
def get_car(
    car_id: int,
    session : Session = Depends(get_session),
):
    car = session.get(Car, car_id)
    if not car: #se não encontrar retorna erro 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Id não encontrado'
        )
    return car


# CRUD [ATUALIZAR]
@router.put(
    path='/{car_id}',
    response_model=CarPublic,
    status_code= status.HTTP_201_CREATED,
)
def update_car(
    car_id: int,
    car:CarSchema,
    session : Session = Depends(get_session),
):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Id não encontrado'
        ) 
    # existir substituir o campo pelo novo valor inserido abaixo no for
    for field, value in car.model_dump().items():
        setattr(db_car, field, value)
    session.commit()
    session.refresh(db_car)
    return db_car