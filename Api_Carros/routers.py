from fastapi import APIRouter, status
#separando as rotas da API
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
def create_car(car: CarSchema):
    return car
