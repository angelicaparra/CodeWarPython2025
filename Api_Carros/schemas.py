from typing import Optional
from pydantic import BaseModel


class CarSchema(BaseModel):
    marca: str
    modelo: str
    ano: Optional[int] = None
    cor: Optional[str] = None
    tipo_combustivel: Optional[str] = None
    modificacao: Optional[str] = None
    descricao: Optional[str] = None

class CarPublic(BaseModel):
    id: int
    marca: str
    modelo: str
    ano: int
    cor: str
    tipo_combustivel: str
    modificacao: str
    descricao: str
