from typing import Optional
from pydantic import BaseModel


class CarSchema(BaseModel):
    marca: str
    modelo: str
    cor: Optional[str] = None
    ano: Optional[int] = None
    tipo_combustivel: Optional[str] = None
    descricao: Optional[str] = None

class CarPublic(BaseModel):
    id: int
    marca: str
    modelo: str
    cor: Optional[str] = None
    ano: Optional[int] = None
    tipo_combustivel: Optional[str] = None
    descricao: Optional[str] = None

class CarPartialUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    cor: Optional[str] = None
    ano: Optional[int] = None
    tipo_combustivel: Optional[str] = None
    descricao: Optional[str] = None


class CarList(BaseModel):
    cars: list[CarPublic]
