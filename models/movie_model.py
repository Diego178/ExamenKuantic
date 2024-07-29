from typing import List
from beanie import Document
from pymongo import ASCENDING
from pydantic import Field, field_validator, model_validator

class Movie(Document):  # This is the model
    name: str = Field(min_length=5, max_length=60)
    director: str = Field(min_length=5, max_length=60)
    gender: List[str] = None
    rating: float = Field(ge=0, le=10)
    year: int = Field(ge=1895, le=2024)
    actors: List[str] = None

    class Settings:
        name = "movies"
        indexes = [
            "director",
            [("year", ASCENDING)]
        ]