from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from Api_Carros.database import get_session
from Api_Carros.models import Car
from Api_Carros.schemas import (
    CarList,
    CarPartialUpdate,
    CarPublic,
    CarSchema,
)

import requests
from fastapi.responses import JSONResponse


router = APIRouter(
    prefix='/api/v1/carros',
    tags=['carros'],
)


# iniciando o Crud [INSERT]
@router.post(
    path='/',
    response_model=CarPublic,
    status_code=status.HTTP_201_CREATED,  # Retorno de Criacao
)
def create_car(
    car: CarSchema, session: Session = Depends(get_session)
):
    # Verificar se carro com mesma marca, modelo e ano já existe
    carro_existente = session.query(Car).filter(
        Car.marca == car.marca,
        Car.modelo == car.modelo,
        Car.ano == car.ano
    ).first()

    if carro_existente:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Carro já cadastrado no sistema."
        )
    # incluindo dependencia do banco
    novo_carro = Car(**car.model_dump())
    session.add(novo_carro)
    session.commit()
    session.refresh(novo_carro)
    return novo_carro

# CRUD [LISTAR]
@router.get(
    path='/',
    response_model=CarList,
    status_code=status.HTTP_200_OK,
)
def list_cars(
    session: Session = Depends(get_session),
    offset: int = 0,  # limitando quantidades de registro quero ver
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
    session: Session = Depends(get_session),
):
    car = session.get(Car, car_id)
    if not car:  # se não encontrar retorna erro 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado'
        )
    return car


# CRUD [ATUALIZAR]
@router.put(
    path='/{car_id}',
    response_model=CarPublic,
    status_code=status.HTTP_201_CREATED,
)
def update_car(
    car_id: int,
    car: CarSchema,
    session: Session = Depends(get_session),
):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado'
        )
    # existir substituir o campo pelo novo valor inserido abaixo no for
    for field, value in car.model_dump().items():
        setattr(db_car, field, value)
    session.commit()
    session.refresh(db_car)
    return db_car


# CRUD [PATCH]
@router.patch(
    path='/{car_id}',
    response_model=CarPublic,
    status_code=status.HTTP_201_CREATED,
)
def patch_car(
    car_id: int,
    car: CarPartialUpdate,
    session: Session = Depends(get_session),
):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado'
        )
    # Utilizando função do python 'Dict Comprehensions'
    # para percorrer a lista, no caso o json e vericar qual item estou alterando
    # e excluo o restante que não foi alterado para assim poder ser inserido
    update_data = {k: v for k, v in car.model_dump(exclude_unset=True).items()}
    for field, value in update_data.items():
        setattr(db_car, field, value)
    session.commit()
    session.refresh(db_car)
    return db_car


# CRUD [DELETE]
@router.delete(
    path='/{car_id}',
    status_code=status.HTTP_204_NO_CONTENT,  # padrao para delete
)
def delete_car(
    car_id: int,
    session: Session = Depends(get_session),
):
    car = session.get(Car, car_id)
    if not car:  # se não encontrar retorna erro 404
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado'
        )
    session.delete(car)
    session.commit()

#API
API_KEY = "bPq0ChpCrtXkh702HFp3wQ==UNRpxWjXTEgOjDLt"
HEADERS = {'X-Api-Key': API_KEY}

@router.post("/etl/importar_carros", status_code=201)
def importar_carros_etl(session: Session = Depends(get_session)):
    url = "https://api.api-ninjas.com/v1/cars"
    params = {"make": "ford"}

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        detalhe_erro = response.text
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao acessar a API externa: {detalhe_erro}"
        )

    dados = response.json()[:5]

    carros_importados = []

    for carro in dados:
        marca = carro.get("make")
        modelo = carro.get("model")
        ano = carro.get("year")

        # Verifica se já existe no banco
        existe = session.query(Car).filter(
            Car.marca == marca,
            Car.modelo == modelo,
            Car.ano == ano
        ).first()

        if existe:
            print(f"Carro {marca} {modelo} {ano} já existe. Pulando importação.")
            continue

        novo_carro = Car(
            marca=marca,
            modelo=modelo,
            cor=None,
            ano=ano,
            tipo_combustivel=carro.get("fuel_type"),
            descricao=f"{marca} {modelo} - {carro.get('fuel_type')} com {carro.get('horsepower', 0)} HP"
        )
        session.add(novo_carro)
        carros_importados.append(modelo)

    session.commit()

    return {
        "importados": len(carros_importados),
        "modelos": carros_importados
    }