from datetime import datetime, timedelta
from bson import ObjectId
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from models.response import exception
import os
from dotenv import load_dotenv
import bcrypt
from connection.connection import collection_users
from logging_config.logging import logger
load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')

outh2_schema = OAuth2PasswordBearer(tokenUrl='token')

def create_token(id: str,type: str):
    to_encode = {
        'id': id,
        'exp': datetime.utcnow() + timedelta(minutes=120),
        'iat': datetime.utcnow(),
        'type': type
        }
    return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

def check_password(password: str, hashed_password: str):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

async def authenticate_user(email: str, password: str):
    print(email)
    user = await collection_users.find_one({'email': email})
    if user is not None:
        if check_password(password, user['password']):
            return user
        else: 
            logger.exception(f"Credentials invalids", exc_info=True)
            raise exception('Credentials invalids', status.HTTP_401_UNAUTHORIZED, True)
    else: 
        logger.exception(f"Credentials invalids", exc_info=True)
        raise exception('Credentials invalids', status.HTTP_401_UNAUTHORIZED, True)    
    

async def get_current_user(token: str = Depends(outh2_schema), *rols):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        expiration = datetime.fromtimestamp(payload['exp'])
        if expiration < datetime.now():
            logger.exception("Session expired")
            raise exception('Session expired', status.HTTP_401_UNAUTHORIZED, True)
        user_id = payload.get('id')
        type = payload.get('type')
        if type in rols:
            user = await collection_users.find_one({'_id': ObjectId(user_id)})
            if user is not None:
                return user
            else:
                logger.exception("User dont found")
                raise exception('User dont found', status.HTTP_401_UNAUTHORIZED, True)
        else:
            name = dict(user).get('name')
            logger.exception("User {name} do not have permissions to access the recource")
            raise exception('You do not have permissions to access this resource', status.HTTP_401_UNAUTHORIZED, True)
    except JWTError as e:
        logger.exception('JWT error: ' + str(e))
        raise exception('JWT error: ' + str(e), status.HTTP_401_UNAUTHORIZED, True)
    
async def get_user(token: str = Depends(outh2_schema)):
    return await get_current_user(token, 'user', 'admin')

async def get_admin_user(token: str = Depends(outh2_schema)):
    return await get_current_user(token, 'admin')