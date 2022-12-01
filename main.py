from fastapi import FastAPI
from db.database import engine
from db.models import Base
from config.db_config import setting
from routers import admin
from routers import staff

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title=setting.TITLE,
    description=setting.DESCRIPTION,
    version=setting.VERSION,
    contact={
        "name": setting.NAME,
        "email": setting.EMAIL
    }
)
app.include_router(admin.router)
app.include_router(staff.router)


@app.get("/")
def hello():
    return {"message": "hello"}
