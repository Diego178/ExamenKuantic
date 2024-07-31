from fastapi.responses import JSONResponse
from pydantic import ValidationError
from auth.authentication import authenticate_user, check_password, create_token
from connection.connection import collection_users
from models.response import Token, exception, message
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from logging_config.logging import logger

router_auth = APIRouter()



@router_auth.post('/token', tags=['auth'], response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if user is not None:
            token = create_token(str(user['_id']), user['type'])
            name = dict(user).get('name')
            logger.info(f"User {name} authenticaded correctly.")
            return Token(access_token= token, token_type = "bearer")
            
    except Exception as e:
        logger.exception(f"Error unexpected: {e}", exc_info=True)
        raise exception("Error unexpected: " + str(e), status.HTTP_500_INTERNAL_SERVER_ERROR, True)
        