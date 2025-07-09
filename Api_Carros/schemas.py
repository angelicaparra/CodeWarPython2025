from typing import Optional
from pydantic import BaseModel


class CarSchema(BaseModel):
    marca: str
    modelo: str
    cor: Optional[str] = None
    ano: Optional[int] = None
    tipo_combustivel: Optional[str] = None
    modificacao: Optional[str] = None
    descricao: Optional[str] = None

class CarPublic(BaseModel):
    id: int
    marca: str
    modelo: str
    cor: str
    ano: int
    tipo_combustivel: str
    modificacao: str
    descricao: str
