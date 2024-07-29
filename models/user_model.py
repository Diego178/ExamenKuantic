from typing import List
from beanie import Document
from pymongo import ASCENDING
from pydantic import Field, field_validator, model_validator, EmailStr

class User(Document):  # This is the model
    name: str = Field(min_length=5, max_length=60)
    email: EmailStr = Field(min_length=5, max_length=60)
    password: List[str] = None
    type: str = Field

    class Settings:
        name = "users"
        indexes = [
            "type",
        ]