from fastapi import FastAPI, Response, status, Depends, HTTPException
from .models import Movies
from sqlalchemy.orm import Session
from .schema import Filme_Model
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from . import database

app = FastAPI()

origins = [
    "http://localhost",  # Permitir localhost
    "http://127.0.0.1:5500",   # ip do server_front
      
]

#Permitir outros acessos 'pingar' na api
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Permitir origens que você especificou
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos os métodos HTTP
    allow_headers=["*"],  # Permitir todos os cabeçalhos
)


#função para obter uma sessão do banco de dados
def get_db():
    db = database.SessionLocal()
    try: 
        yield db
    finally:
        db.close()


#Root da api
@app.get('/')
def retornar_root():
    return{'Uma API feita por': 'Kauan Afonso😎'}


#Criar um filme
@app.post('/filmes/', response_model=Filme_Model , status_code=201)
def create_movie(movie: Filme_Model, response:Response, db: Session = Depends(get_db)):
    #tentar pegar todos os dados da api, adicionar ao banco salvar e recarrega-lo
    try:
        db_movie = Movies(name=movie.name, director=movie.director, year=movie.year, gender=movie.gender, actors=movie.actors, ratings=movie.ratings)
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie
    except:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'error':'Invalid datas'}
        
#Pegando todos os flmes
@app.get('/filmes/')
def get_movies(db:Session = Depends(get_db)):
    data = db.query(Movies).all()
    return data


#Obtendo um filme
@app.get('/filmes/{id}', status_code=status.HTTP_200_OK)
def get_movies_id(id:int, response:Response, db:Session = Depends(get_db)):
    try:
        data = db.query(Movies).get(id)
        if not data:
            response.status_code = status.HTTP_404_NOT_FOUND
            raise HTTPException(status_code=404, detail='movie not found') #lançando um erro de http -> pois somente com try_catch não estava retornando o status correto
            
        return data
    except Exception as e:
        return {'erro': e}
    

#atualizando um filme
@app.put('/filmes/{id}', response_model=Filme_Model, status_code=status.HTTP_200_OK)
def update_movie(id:int, response:Response, movie:Filme_Model, db:Session = Depends(get_db)):


    data = db.query(Movies).get(id) #obtendo o filme
      
    if not data:
        # Se não encontrar o filme, levanta um erro 404
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found")
    
    data.name = movie.name
    data.director = movie.director
    data.year = movie.year
    data.gender = movie.gender
    data.actors = movie.actors
    data.ratings = movie.ratings

    db.commit()
    db.refresh(data)
    return data


#Deletando um movie
@app.delete('/filmes/{id}', status_code=status.HTTP_200_OK)
def delete_movie(id:int , response:Response, db:Session = Depends(get_db)):
    try:
        movie_selected = db.query(Movies).get(id) #obtendo o movie
        db.delete(movie_selected) #deletando ele 
        db.commit()
        return{f"Deletado com sucesso: {movie_selected}"}#Retornando o nome
    except:
        response.status_code = status.HTTP_404_NOT_FOUND
        return{'error': 'movie not found!'} #tratando caso não encontre