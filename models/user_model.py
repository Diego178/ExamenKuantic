from beanie import Document
from pydantic import Field, field_validator, model_validator, EmailStr

class User(Document):
    name: str = Field(min_length=0, max_length=60)
    email: EmailStr = Field(min_length=0, max_length=60)
    password: str = Field(min_length=0, max_length=150)
    type: str = Field(min_length=0, max_length=10)
    
    @field_validator("type")
    @classmethod
    def type_valid(cls, v: str) -> str:
        if v not in ["user",  "admin"]:
            raise ValueError("Type not valid, should be: user or admin")
        else:
            return v

    class Settings:
        name = "collection_users"
        indexes = [
            "type",
        ]