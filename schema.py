from pydantic import BaseModel
from typing import List


#modelo de como os dados devem ser enviados
class Filme_Model(BaseModel):
    name: str
    director: str
    year: int
    gender: str
    actors: str
    ratings: float  # Alterando de str para float

    class Config:
        orm_mode = True #converte para instancia do sqlalchemy