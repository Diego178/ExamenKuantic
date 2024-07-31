import bcrypt
from bson import ObjectId
from bson.errors import InvalidId
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from auth.authentication import get_admin_user
from models.response import message, exception
from models.user_model import User 
from fastapi import APIRouter, Depends, status
from connection.connection import collection_users
from logging_config.logging import logger

from schemas.user_schema import list_serial_users

router_user = APIRouter()

@router_user.post('/users', tags=['users'], response_class=JSONResponse)
async def post_user(user: User):
    try:
        new_user = dict(user)
        user_db = await collection_users.find_one({"email": new_user["email"]})
        
        if user_db is None:
            if len(new_user['password']) < 8:
                logger.exception("The passwors is invalid")
                raise exception('Password short, should have min 8 caracters', status.HTTP_400_BAD_REQUEST, True)
            salt = bcrypt.gensalt()
            password =  bcrypt.hashpw(new_user['password'].encode('utf-8'), salt)
            new_user['password'] = password.decode('utf-8')
            await collection_users.insert_one(new_user)
            logger.info(f"User created. Type: {new_user['type']}")
            return message("User created correctly", status.HTTP_201_CREATED, False)
        else:
            logger.exception("The email is in use, try with another one")
            return message("The email is in use, try with another one", status.HTTP_200_OK, False)
    except ValidationError as e:
        logger.exception(f'Validation error: {e}')
        raise exception(f'Validation error: {e}', status.HTTP_422_UNPROCESSABLE_ENTITY, True)
        
@router_user.delete('/users/{id}', tags=['users'], response_class=JSONResponse)
async def delete_user(id: str, user: User = Depends(get_admin_user)):
    name = dict(user).get('name')
    id_auth = dict(user).get('_id')
    try:
        user_bd = await collection_users.find_one({'_id': ObjectId(id)})
        if str(id_auth) == id:
            logger.exception(f'The User {name} couldnt deleted the user {dict(user_bd).get('name')}, becouse has a session active')
            raise exception('Cannot deleted this user, becouse has a session active', status.HTTP_404_NOT_FOUND, True)
        if user_bd is None:
            raise exception('User dont found', status.HTTP_404_NOT_FOUND, True) 
        await collection_users.delete_one({"_id": ObjectId(id)})
        logger.info(f"User {name} deleted a user.")
        return message("User deleted correctly", status.HTTP_200_OK, False)
    except InvalidId:
        logger.exception(f"User {name} attempted to delet a other user with an invalid ID.")
        raise exception('Invalid id', status.HTTP_422_UNPROCESSABLE_ENTITY, True)
    
@router_user.get('/users', tags=['users'], response_model=list[User])
async def get_users(user: User = Depends(get_admin_user)):
    name = dict(user).get('name')
    logger.info(f"User {name} gets all the users.")
    return await list_serial_users(collection_users.find())