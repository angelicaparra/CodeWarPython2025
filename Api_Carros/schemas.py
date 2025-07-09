from pydantic import BaseModel


class CarSchema(BaseModel):
    modelo: str
    descricao: str
    marca: str
    ano: int
    cor: str
    tipo_combustivel: str
    modificacao: str
