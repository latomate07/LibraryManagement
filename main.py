from fastapi import FastAPI
import uvicorn
from routers import books, users, loans
from config.settings import settings

app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

app.include_router(books.router, prefix="/books", tags=["Books"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(loans.router, prefix="/loans", tags=["Loans"])

@app.get("/")
def read_root():
    return {
        "message": "Bienvenue dans l'API de gestion de bibliothèque",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)