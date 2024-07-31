from typing import List, Optional
from beanie import Document
from bson import ObjectId
from pymongo import ASCENDING
from pydantic import Field, field_validator, model_validator


class Movie(Document):
    _id: Optional[ObjectId] = None
    name: str = Field(min_length=5, max_length=60)
    director: str = Field(min_length=5, max_length=60)
    gender: List[str] = Field(default_factory=list)
    rating: float = Field(ge=0, le=10)
    year: int = Field(ge=1895, le=2024)
    actors: List[str] = Field(default_factory=list)

    class Settings:
        name = "collection_movies"
        indexes = [
            "director",
            [("year", ASCENDING)]
        ]