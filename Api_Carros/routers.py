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

router = APIRouter(
    prefix='/api/v1/carros',
    tags=['carros'],
)

# Configuração da API externa
API_KEY = "bPq0ChpCrtXkh702HFp3wQ==UNRpxWjXTEgOjDLt"
HEADERS = {'X-Api-Key': API_KEY}

# CRUD [CREATE]
@router.post('/', response_model=CarPublic, status_code=status.HTTP_201_CREATED)
def create_car(car: CarSchema, session: Session = Depends(get_session)):
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

    novo_carro = Car(**car.model_dump())
    session.add(novo_carro)
    session.commit()
    session.refresh(novo_carro)
    return novo_carro

# CRUD [READ - LISTAR TODOS (internos + externos)]
@router.get("/todos", status_code=200)
def listar_todos_os_carros(session: Session = Depends(get_session)):
    try:
        locais = session.scalars(select(Car)).all()

        url = "https://api.api-ninjas.com/v1/cars"
        params = {"make": "ford"}
        response = requests.get(url, headers=HEADERS, params=params)

        if response.status_code != 200:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Erro da API externa: {response.text}"
            )

        externos = response.json()
        if not isinstance(externos, list):
            raise HTTPException(status_code=500, detail="Resposta inesperada da API externa")

        return {
            "locais": [CarPublic.from_orm(car).dict() for car in locais],
            "externos": externos[:5]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")

# CRUD [READ - PAGINADO]
@router.get('/', response_model=CarList, status_code=status.HTTP_200_OK)
def list_cars(session: Session = Depends(get_session), offset: int = 0, limit: int = 100):
    query = session.scalars(select(Car).offset(offset).limit(limit))
    cars = query.all()
    return {'cars': cars}

# CRUD [READ - POR ID]
@router.get('/{car_id}', response_model=CarPublic, status_code=status.HTTP_200_OK)
def get_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')
    return car

# CRUD [UPDATE]
@router.put('/{car_id}', response_model=CarPublic, status_code=status.HTTP_201_CREATED)
def update_car(car_id: int, car: CarSchema, session: Session = Depends(get_session)):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')

    for field, value in car.model_dump().items():
        setattr(db_car, field, value)
    session.commit()
    session.refresh(db_car)
    return db_car

# CRUD [PATCH]
@router.patch('/{car_id}', response_model=CarPublic, status_code=status.HTTP_201_CREATED)
def patch_car(car_id: int, car: CarPartialUpdate, session: Session = Depends(get_session)):
    db_car = session.get(Car, car_id)
    if not db_car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')

    update_data = {k: v for k, v in car.model_dump(exclude_unset=True).items()}
    for field, value in update_data.items():
        setattr(db_car, field, value)
    session.commit()
    session.refresh(db_car)
    return db_car

# CRUD [DELETE]
@router.delete('/{car_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, session: Session = Depends(get_session)):
    car = session.get(Car, car_id)
    if not car:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Id não encontrado')
    session.delete(car)
    session.commit()

# [ETL] Importar da API Externa
@router.post("/etl/importar_carros", status_code=201)
def importar_carros_etl(session: Session = Depends(get_session)):
    url = "https://api.api-ninjas.com/v1/cars"
    params = {"make": "ford"}

    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=f"Erro ao acessar a API externa: {response.text}"
        )

    dados = response.json()[:5]
    carros_importados = []

    for carro in dados:
        marca = carro.get("make")
        modelo = carro.get("model")
        ano = carro.get("year")

        existe = session.query(Car).filter(
            Car.marca == marca,
            Car.modelo == modelo,
            Car.ano == ano
        ).first()

        if existe:
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

# [IMPORTAÇÃO EM LOTE]
@router.post("/importar-lote", status_code=201)
def importar_lote(carros: list[CarSchema], session: Session = Depends(get_session)):
    carros_salvos = []
    for carro in carros:
        novo_carro = Car(**carro.model_dump())
        session.add(novo_carro)
        carros_salvos.append(carro.modelo)

    session.commit()
    return {"importados": len(carros_salvos), "modelos": carros_salvos}
