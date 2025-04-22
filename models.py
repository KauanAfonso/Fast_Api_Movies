from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base() #Cria uma classe base que será herdada para outras classes


#Tabela de movies 
class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name =Column(String, index=True)
    director = Column(String, index=True)
    year = Column(Integer, index=True)
    gender = Column(String, index=True)
    actors= Column(String, index =True)
    ratings = Column(Float, index=True)

    