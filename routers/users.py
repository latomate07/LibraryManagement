from fastapi import APIRouter, HTTPException, Path, Response
from typing import List
from datetime import date

from schemas.user import User, UserCreate, UserUpdate
from schemas.loan import Loan
from db.database import users_db, loans_db, find_item_by_id, find_item_index, get_next_id
from models.enums import LoanStatus

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_users():
    """Récupérer tous les utilisateurs"""
    return users_db


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int = Path(..., gt=0)):
    """Récupérer les détails d'un utilisateur spécifique"""
    user = find_item_by_id(users_db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return user


@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    """Ajouter un nouvel utilisateur"""
    # Vérifier si l'email existe déjà
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(
                status_code=400,
                detail="Un utilisateur avec cet email existe déjà"
            )

    user_id = get_next_id(users_db)
    new_user = user.dict()
    new_user["id"] = user_id
    new_user["registration_date"] = date.today()
    users_db.append(new_user)
    return new_user


@router.put("/{user_id}", response_model=User)
async def update_user(user_data: UserUpdate, user_id: int = Path(..., gt=0)):
    """Mettre à jour les informations d'un utilisateur"""
    index = find_item_index(users_db, user_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Mise à jour partielle
    user = users_db[index]
    update_data = user_data.dict(exclude_unset=True)

    # Vérifier si l'email mis à jour existe déjà
    if "email" in update_data and update_data["email"] != user["email"]:
        email_exists = any(
            u["email"] == update_data["email"] and u["id"] != user_id
            for u in users_db
        )
        if email_exists:
            raise HTTPException(
                status_code=400,
                detail="Un utilisateur avec cet email existe déjà"
            )

    # Appliquer les modifications
    updated_user = {**user, **update_data}
    users_db[index] = updated_user

    return updated_user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int = Path(..., gt=0)):
    """Supprimer un utilisateur"""
    index = find_item_index(users_db, user_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    # Vérifier si l'utilisateur a des emprunts actifs
    for loan in loans_db:
        if loan["user_id"] == user_id and loan["status"] == LoanStatus.ACTIVE:
            raise HTTPException(
                status_code=400,
                detail="Impossible de supprimer l'utilisateur car il a des emprunts actifs"
            )

    users_db.pop(index)
    return Response(status_code=204)


@router.get("/{user_id}/loans", response_model=List[Loan])
async def get_user_loans(user_id: int = Path(..., gt=0)):
    """Récupérer tous les emprunts d'un utilisateur spécifique"""
    # Vérifier si l'utilisateur existe
    user = find_item_by_id(users_db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

    return [loan for loan in loans_db if loan["user_id"] == user_id]