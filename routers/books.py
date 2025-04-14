from fastapi import APIRouter, HTTPException, Path, Query, Response
from typing import List, Optional

from schemas.book import Book, BookCreate, BookUpdate
from db.database import books_db, loans_db, find_item_by_id, find_item_index, get_next_id
from models.enums import LoanStatus

router = APIRouter()


@router.get("/", response_model=List[Book])
async def get_books(available: Optional[bool] = None):
    """Récupérer tous les livres, avec option de filtrer par disponibilité"""
    if available is None:
        return books_db
    return [book for book in books_db if book["available"] == available]


@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int = Path(..., gt=0, description="ID du livre à récupérer")):
    """Récupérer les détails d'un livre spécifique"""
    book = find_item_by_id(books_db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre non trouvé")
    return book


@router.post("/", response_model=Book, status_code=201)
async def create_book(book: BookCreate):
    """Ajouter un nouveau livre"""
    book_id = get_next_id(books_db)
    new_book = book.dict()
    new_book["id"] = book_id
    books_db.append(new_book)
    return new_book


@router.put("/{book_id}", response_model=Book)
async def update_book(book_data: BookUpdate, book_id: int = Path(..., gt=0)):
    """Mettre à jour les informations d'un livre"""
    index = find_item_index(books_db, book_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    # Mise à jour partielle
    book = books_db[index]
    update_data = book_data.dict(exclude_unset=True)

    # Vérifier si la mise à jour de la disponibilité est cohérente avec les emprunts actifs
    if "available" in update_data and update_data["available"] and not book["available"]:
        # Vérifier si le livre est actuellement emprunté
        active_loan = any(
            loan["book_id"] == book_id and loan["status"] == LoanStatus.ACTIVE
            for loan in loans_db
        )
        if active_loan:
            raise HTTPException(
                status_code=400,
                detail="Impossible de rendre le livre disponible car il est actuellement emprunté"
            )

    # Appliquer les modifications
    updated_book = {**book, **update_data}
    books_db[index] = updated_book

    return updated_book


@router.delete("/{book_id}", status_code=204)
async def delete_book(book_id: int = Path(..., gt=0)):
    """Supprimer un livre"""
    index = find_item_index(books_db, book_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Livre non trouvé")

    # Vérifier si le livre est actuellement emprunté
    for loan in loans_db:
        if loan["book_id"] == book_id and loan["status"] == LoanStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail="Impossible de supprimer le livre car il est actuellement emprunté"
            )

    books_db.pop(index)
    return Response(status_code=204)