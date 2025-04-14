from pydantic import BaseModel, Field
from datetime import date
from typing import Optional
from models.enums import LoanStatus


class LoanBase(BaseModel):
    book_id: int = Field(..., gt=0, description="Identifiant du livre")
    user_id: int = Field(..., gt=0, description="Identifiant de l'utilisateur")


class LoanCreate(LoanBase):
    pass


class LoanUpdate(BaseModel):
    return_date: Optional[date] = None
    status: Optional[LoanStatus] = None


class Loan(LoanBase):
    id: int = Field(..., description="Identifiant unique de l'emprunt")
    loan_date: date = Field(..., description="Date d'emprunt")
    return_date: date = Field(..., description="Date de retour prévue")
    status: LoanStatus = Field(..., description="Statut de l'emprunt")

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "book_id": 3,
                "user_id": 2,
                "loan_date": "2023-04-01",
                "return_date": "2023-04-15",
                "status": "active"
            }
        }