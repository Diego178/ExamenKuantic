from bson import ObjectId
from bson.errors import InvalidId
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from auth.authentication import get_admin_user, get_user
from connection.connection import collection_movies
from models.movie_model import Movie
from models.response import exception, message
from models.user_model import User
from schemas.movie_schema import list_serial_movies
from fastapi import APIRouter, Depends, status

router_movie = APIRouter()


@router_movie.get('/movies', tags=['movies'], response_model=list[Movie])
async def get_movies(user: User = Depends(get_user)):
    return await list_serial_movies(collection_movies.find())

@router_movie.post('/movies', tags=['movies'], response_class=JSONResponse)
async def post_movie(movie: Movie , user: User= Depends(get_admin_user)):
    try:
        if len(movie.actors) == 0:
            return JSONResponse(status_code=400, content={"message": "Actors list cannot be empty", "error": True})
        if len(movie.gender) == 0:
            return JSONResponse(status_code=400, content={"message": "Genders list cannot be empty", "error": True})
        collection_movies.insert_one(dict(movie))
        return JSONResponse(status_code=201, content={"message": "Movie registered correctly", "error": False})
    except ValidationError as e:
        raise exception('Validation error: ' + str(e), status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    

@router_movie.put('/movies/{id}', tags=['movies'], response_class=JSONResponse)
async def put_movie(id: str, movie: Movie, user: User= Depends(get_admin_user)):
    try:
        movie_db = await collection_movies.find_one({'_id': ObjectId(id)})
        if movie_db is None:
            raise exception('Movie dont found', status.HTTP_404_NOT_FOUND, True) 
        else:
            await collection_movies.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(movie)})
            return message('Movie updated correctly', status.HTTP_200_OK, False)
    except ValidationError as e:
        raise exception('Validation error: ' + str(e), status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    except InvalidId:
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)

@router_movie.delete('/movies/{id}', tags=['movies'])
async def delete_movie(id: str, user: User= Depends(get_admin_user)):
    try: 
        movie_db = await collection_movies.find_one({'_id': ObjectId(id)})
        if movie_db is None:
            raise exception('Movie dont found', status.HTTP_404_NOT_FOUND, True) 
        await collection_movies.find_one_and_delete({'_id': ObjectId(id)})
        return message('Movie deleted correctly', status.HTTP_200_OK, False)
    except InvalidId:
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)