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
from logging_config.logging import logger


router_movie = APIRouter()


@router_movie.get('/movies', tags=['movies'], response_model=list[Movie])
async def get_movies(user: User = Depends(get_user)):
    name = dict(user).get('name')
    logger.info(f"User {name} gets movies correctly.")
    return await list_serial_movies(collection_movies.find())

@router_movie.get('/movies/{id}', tags=['movies'], response_model=Movie)
async def get_movie_by_id(id:str, user: User = Depends(get_user)):
    name = dict(user).get('name')
    try:
        movie = await collection_movies.find_one({'_id': ObjectId(id)})
        if movie is None:
            logger.exception(f"User {name} tried to access a movie that was not found.")
            raise exception('Movie dont found', status.HTTP_404_NOT_FOUND, True)
        logger.info(f"User {name} retrieved a movie successfully.") 
        return movie
    except InvalidId:
        logger.exception(f"User {name} attempted to retrieve a movie with an invalid ID.")
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)


@router_movie.post('/movies', tags=['movies'], response_class=JSONResponse)
async def post_movie(movie: Movie , user: User= Depends(get_admin_user)):
    name = dict(user).get('name')
    try:
        new_movie = dict(movie)
        movie_db = await collection_movies.find_one({'name': new_movie['name']})
        if movie_db is not None:
            logger.exception(f"User {name} tried to create a movie but the name is already used.")
            raise exception('The movie name is already used', status.HTTP_409_CONFLICT, True) 
        
        if len(movie.actors) == 0:
            logger.error(f"User {name} tried to create a movie but the array of actors was empty.")
            return JSONResponse(status_code=400, content={"message": "Actors list cannot be empty", "error": True})
        if len(movie.gender) == 0:
            logger.error(f"User {name} tried to create a movie but the array of gender was empty.")
            return JSONResponse(status_code=400, content={"message": "Genders list cannot be empty", "error": True})
        
        await collection_movies.insert_one(dict(movie))
        logger.info(f"User {name} create a movie correctly.")
        return JSONResponse(status_code=201, content={"message": "Movie registered correctly", "error": False})
    except ValidationError as e:
        logger.exception(f"User {name} tried to create a movie but has validation errors.")
        raise exception('Validation error: ' + str(e), status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    

@router_movie.put('/movies/{id}', tags=['movies'], response_class=JSONResponse)
async def put_movie(id: str, movie: Movie, user: User= Depends(get_admin_user)):
    name = dict(user).get('name')
    try:
        movie_db = await collection_movies.find_one({'_id': ObjectId(id)})
        if movie_db is None:
            logger.exception(f"User {name} tried to access a movie that was not found.")
            raise exception('Movie dont found', status.HTTP_404_NOT_FOUND, True) 
        else:
            await collection_movies.find_one_and_update({'_id': ObjectId(id)}, {'$set': dict(movie)})
            logger.info(f"User {name} update a movie correctly.")
            return message('Movie updated correctly', status.HTTP_200_OK, False)
    except ValidationError as e:
        logger.exception(f"User {name} tried to update a movie but has validation errors.")
        raise exception('Validation error: ' + str(e), status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    except InvalidId:
        logger.exception(f"User {name} attempted to retrieve a movie with an invalid ID.")
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)

@router_movie.delete('/movies/{id}', tags=['movies'])
async def delete_movie(id: str, user: User= Depends(get_admin_user)):
    name = dict(user).get('name')
    try: 
        movie_db = await collection_movies.find_one({'_id': ObjectId(id)})
        if movie_db is None:
            logger.exception(f"User {name} tried to access a movie that was not found.")
            raise exception('Movie dont found', status.HTTP_404_NOT_FOUND, True) 
        await collection_movies.find_one_and_delete({'_id': ObjectId(id)})
        logger.info(f"User {name} delete a movie correctly.")
        return message('Movie deleted correctly', status.HTTP_200_OK, False)
    except InvalidId:
        logger.exception(f"User {name} attempted to retrieve a movie with an invalid ID.")
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)