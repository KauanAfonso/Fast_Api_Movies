from pydantic import BaseModel, Field
from typing import List



'''

Modelo de como os dados devem ser enviados para lidar com o filmes
Adicionando formas de campos esperados.

'''
class Filme_Model(BaseModel):
    name: str = Field(title="Nome do filme", max_length=255)
    director: str = Field(title="Diretor do filme", max_length=255)
    year: int = Field(title="Ano do filme")
    gender: str | None = Field(default=None, title="Genero od item", max_length=100)
    actors: str = Field(title="Atores do filme", max_length=255)
    ratings: float = Field(title="Nota do filme")

    class Config:
        orm_mode = True #converte para instancia do sqlalchemy

