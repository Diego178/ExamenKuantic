from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from pydantic import BaseModel

def message(message: str, status: status, error: bool, data = None):
    return JSONResponse(
        status_code=status, 
        content={
            "message": message, 
            "error": error,
            "data": data})
def exception(message: str, status: status, error: bool):
    return HTTPException(
        status_code=status, 
        detail={
            "message": message, 
            "error": error})

class Token(BaseModel):
    access_token: str
    token_type: str