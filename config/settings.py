from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_TITLE: str = "Library Management API"
    APP_DESCRIPTION: str = "API RESTful pour la gestion d'une bibliothèque"
    APP_VERSION: str = "1.0.0"

    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True

    class Config:
        env_file = ".env"


settings = Settings()