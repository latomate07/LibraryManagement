from datetime import date, timedelta
from typing import Dict, List, Optional, Any

from models.enums import LoanStatus

# Simulation de base de données avec des listes de dictionnaires
books_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "title": "Le Petit Prince",
        "author": "Antoine de Saint-Exupéry",
        "publication_date": date(1943, 4, 6),
        "category": "Fiction",
        "available": True
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "publication_date": date(1949, 6, 8),
        "category": "Science-Fiction",
        "available": True
    },
    {
        "id": 3,
        "title": "L'Étranger",
        "author": "Albert Camus",
        "publication_date": date(1942, 5, 19),
        "category": "Philosophie",
        "available": False
    }
]

users_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "name": "Marie Dupont",
        "email": "marie.dupont@email.com",
        "phone": "0612345678",
        "registration_date": date(2022, 1, 15)
    },
    {
        "id": 2,
        "name": "Jean Martin",
        "email": "jean.martin@email.com",
        "phone": "0687654321",
        "registration_date": date(2022, 3, 20)
    }
]

loans_db: List[Dict[str, Any]] = [
    {
        "id": 1,
        "book_id": 3,
        "user_id": 2,
        "loan_date": date(2023, 4, 1),
        "return_date": date(2023, 4, 15),
        "status": LoanStatus.ACTIVE
    }
]

# Fonctions utilitaires pour manipuler les données

def get_next_id(db_list: List[Dict[str, Any]]) -> int:
    """Génère le prochain ID disponible pour une nouvelle entrée"""
    return max([item["id"] for item in db_list], default=0) + 1

def find_item_by_id(db_list: List[Dict[str, Any]], item_id: int) -> Optional[Dict[str, Any]]:
    """Recherche un élément par son ID"""
    for item in db_list:
        if item["id"] == item_id:
            return item
    return None

def find_item_index(db_list: List[Dict[str, Any]], item_id: int) -> Optional[int]:
    """Recherche l'index d'un élément par son ID"""
    for index, item in enumerate(db_list):
        if item["id"] == item_id:
            return index
    return None