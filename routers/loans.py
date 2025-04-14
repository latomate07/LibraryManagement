from fastapi import APIRouter, HTTPException, Path, Query, Response
from typing import List, Optional
from datetime import date, timedelta

from schemas.loan import Loan, LoanCreate, LoanUpdate
from db.database import loans_db, books_db, users_db, find_item_by_id, find_item_index, get_next_id
from models.enums import LoanStatus

router = APIRouter()


@router.get("/", response_model=List[Loan])
async def get_loans(status: Optional[LoanStatus] = None):
    """Récupérer tous les emprunts, avec option de filtrer par statut"""
    if status is None:
        return loans_db
    return [loan for loan in loans_db if loan["status"] == status]


@router.get("/{loan_id}", response_model=Loan)
async def get_loan(loan_id: int = Path(..., gt=0)):
    """Récupérer les détails d'un emprunt spécifique"""
    loan = find_item_by_id(loans_db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")
    return loan


@router.post("/", response_model=Loan, status_code=201)
async def create_loan(loan: LoanCreate):
    """Créer un nouvel emprunt"""
    # Vérifier si le livre existe
    book = find_item_by_id(books_db, loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    # Vérifier si le livre est disponible
    if not book["available"]:
        raise HTTPException(status_code=400, detail="Le livre n'est pas disponible")

    # Vérifier si l'utilisateur existe
    user = find_item_by_id(users_db, loan.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Créer l'emprunt
    loan_id = get_next_id(loans_db)
    today = date.today()
    return_date = today + timedelta(days=14)  # 2 semaines par défaut

    new_loan = {
        "id": loan_id,
        "book_id": loan.book_id,
        "user_id": loan.user_id,
        "loan_date": today,
        "return_date": return_date,
        "status": LoanStatus.ACTIVE
    }

    # Mettre à jour la disponibilité du livre
    book_index = find_item_index(books_db, loan.book_id)
    books_db[book_index]["available"] = False

    loans_db.append(new_loan)
    return new_loan


@router.put("/{loan_id}/return", response_model=Loan)
async def return_book(loan_id: int = Path(..., gt=0)):
    """Marquer un livre comme retourné"""
    loan_index = find_item_index(loans_db, loan_id)
    if loan_index is None:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")

    loan = loans_db[loan_index]
    if loan["status"] != LoanStatus.ACTIVE:
        raise HTTPException(
            status_code=400,
            detail="Ce livre a déjà été retourné ou a un autre statut"
        )

    # Mettre à jour le statut de l'emprunt
    loans_db[loan_index]["status"] = LoanStatus.RETURNED

    # Rendre le livre disponible à nouveau
    book_index = find_item_index(books_db, loan["book_id"])
    if book_index is not None:  # Le livre pourrait avoir été supprimé
        books_db[book_index]["available"] = True

    return loans_db[loan_index]


@router.put("/{loan_id}", response_model=Loan)
async def update_loan(loan_data: LoanUpdate, loan_id: int = Path(..., gt=0)):
    """Mettre à jour les informations d'un emprunt"""
    loan_index = find_item_index(loans_db, loan_id)
    if loan_index is None:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")

    # Mise à jour partielle
    loan = loans_db[loan_index]
    update_data = loan_data.dict(exclude_unset=True)

    # Si on change le statut d'ACTIVE à autre chose, rendre le livre disponible
    if "status" in update_data and update_data["status"] != LoanStatus.ACTIVE and loan["status"] == LoanStatus.ACTIVE:
        book_index = find_item_index(books_db, loan["book_id"])
        if book_index is not None:
            books_db[book_index]["available"] = True

    # Appliquer les modifications
    updated_loan = {**loan, **update_data}
    loans_db[loan_index] = updated_loan

    return updated_loan


@router.delete("/{loan_id}", status_code=204)
async def delete_loan(loan_id: int = Path(..., gt=0)):
    """Supprimer un emprunt"""
    loan_index = find_item_index(loans_db, loan_id)
    if loan_index is None:
        raise HTTPException(status_code=404, detail="Emprunt non trouvé")

    loan = loans_db[loan_index]

    # Si l'emprunt est actif, rendre le livre disponible
    if loan["status"] == LoanStatus.ACTIVE:
        book_index = find_item_index(books_db, loan["book_id"])
        if book_index is not None:
            books_db[book_index]["available"] = True

    loans_db.pop(loan_index)
    return Response(status_code=204)