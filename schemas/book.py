from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Titre du livre")
    author: str = Field(..., min_length=1, max_length=100, description="Auteur du livre")
    publication_date: date = Field(..., description="Date de publication")
    category: str = Field(..., min_length=1, max_length=50, description="Catégorie du livre")
    available: bool = Field(True, description="Disponibilité du livre")


class BookCreate(BookBase):
    pass


class BookUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    publication_date: Optional[date] = None
    category: Optional[str] = Field(None, min_length=1, max_length=50)
    available: Optional[bool] = None


class Book(BookBase):
    id: int = Field(..., description="Identifiant unique du livre")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Le Petit Prince",
                "author": "Antoine de Saint-Exupéry",
                "publication_date": "1943-04-06",
                "category": "Fiction",
                "available": True
            }
        }