from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from Api_Carros.database import get_session
from Api_Carros.models import Car
from Api_Carros.schemas import (
    CarPublic,
    CarSchema,
)

router = APIRouter(
    prefix='/api/v1/carros',
    tags=['carros'],
)

#iniciando o Crud
@router.post(
        path='/', 
        response_model=CarPublic, 
        status_code=status.HTTP_201_CREATED,
)
def create_car(car: CarSchema,session: Session = Depends(get_session)): #incluindo dependencia do banco
    car = Car(**car.model_dump())
    session.add(car)
    session.commit()
    session.refresh(car)
    return car

