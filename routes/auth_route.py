from fastapi.responses import JSONResponse
from pydantic import ValidationError
from auth.authentication import authenticate_user, check_password, create_token
from connection.connection import collection_users
from models.response import Token, message
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

router_auth = APIRouter()



@router_auth.post('/token', tags=['auth'], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if user is not None:
            token = create_token(str(user['_id']), user['type'])
            return Token(access_token= token, token_type = "bearer")
            
    except ValidationError as e:
        print(e)
        