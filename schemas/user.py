from pydantic import BaseModel, Field, EmailStr
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Nom de l'utilisateur")
    email: str = Field(..., min_length=5, max_length=100, description="Email de l'utilisateur")
    phone: str = Field(..., min_length=8, max_length=20, description="Numéro de téléphone")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=5, max_length=100)
    phone: Optional[str] = Field(None, min_length=8, max_length=20)


class User(UserBase):
    id: int = Field(..., description="Identifiant unique de l'utilisateur")
    registration_date: date = Field(..., description="Date d'inscription")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Marie Dupont",
                "email": "marie.dupont@email.com",
                "phone": "0612345678",
                "registration_date": "2022-01-15"
            }
        }