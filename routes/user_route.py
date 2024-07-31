import bcrypt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from auth.authentication import get_admin_user
from models.response import message, exception
from models.user_model import User
from schemas.movie_schema import list_serial_movies
from fastapi import APIRouter, Depends, status
from connection.connection import collection_users
import os

from schemas.user_schema import list_serial_users

router_user = APIRouter()

@router_user.post('/users', tags=['users'], response_class=JSONResponse)
async def post_user(user: User):
    try:
        new_user = dict(user)
        user_db = await collection_users.find_one({"email": new_user["email"]})
        
        if user_db is None:
            if len(new_user['password']) < 8:
                raise exception('Password short, should have min 8 caracters', status.HTTP_400_BAD_REQUEST, True)
            salt = bcrypt.gensalt()
            password =  bcrypt.hashpw(new_user['password'].encode('utf-8'), salt)
            new_user['password'] = password.decode('utf-8')
            await collection_users.insert_one(new_user)
            return message("User created correctly", status.HTTP_201_CREATED, False)
        return message("The email is in use, try with another one", status.HTTP_200_OK, False)
    except ValidationError as e:
        print(e)
        
@router_user.delete('/users/{id}', tags=['users'], response_class=JSONResponse)
async def delete_user(id: str, user: User = Depends(get_admin_user)):
    try:
        user_bd = await collection_users.find_one({'_id': ObjectId(id)})
        if user_bd is None:
            raise exception('User dont found', status.HTTP_404_NOT_FOUND, True) 
        await collection_users.delete_one({"_id": ObjectId(id)})
        return message("User deleted correctly", status.HTTP_200_OK, False)
    except InvalidId:
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    
@router_user.get('/users', tags=['users'], response_model=list[User])
async def get_users(user: User = Depends(get_admin_user)):
    return await list_serial_users(collection_users.find())