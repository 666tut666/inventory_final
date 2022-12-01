import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")
    #loding .env file


class Settings:
    TITLE="Inventory Management using FastAPI"
    VERSION="0.0.1"
    DESCRIPTION="testing"
    NAME="user"
    EMAIL="samipya95@gmail.com"

    POSTGRES_USER = os.getenv("POSTGRES_USER")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "inventory_management")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DATABASE}"


setting = Settings()
