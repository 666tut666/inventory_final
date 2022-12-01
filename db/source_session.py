from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.db_config import db_cfg

# for local connection

# SQLALCHEMY_DATABASE_URL = \
#     f"mssql+pyodbc://{db_cfg.DB_USER}:{db_cfg.DB_PASSWORD}@{db_cfg.DB_HOST_LOCAL}:{db_cfg.DB_PORT_LOCAL}/{db_cfg.DB_NAME}?driver={db_cfg.DB_DRIVER}"

# for docker connection

SQLALCHEMY_DATABASE_URL = \
    f"mssql+pyodbc://{db_cfg.DB_USER}:{db_cfg.DB_PASSWORD}@{db_cfg.DB_HOST}:{db_cfg.DB_PORT}/{db_cfg.DB_NAME}?driver={db_cfg.DB_DRIVER}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator:
    session = SessionLocal()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
