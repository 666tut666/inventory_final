from fastapi import FastAPI
from db.database import engine
from db.models import Base
from config.db_config import setting

from routers import admin
from routers import items
from routers import login
from routers import users
from routers import request
from webapps.routers import items as web_items, admin as web_users, auth as web_auth
from fastapi.staticfiles import StaticFiles

from fastapi.middleware.cors import CORSMiddleware


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

app.mount("/static", StaticFiles(directory="static"), name="static")
    #mount the path for img


origins = [    "http://localhost",    "http://localhost:8000",    "http://localhost:3000",    "https://example.com",    "https://www.example.com",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(items.router)
app.include_router(users.router)
app.include_router(web_items.router)
app.include_router(web_users.router)
app.include_router(web_auth.router)
app.include_router(request.router)
app.include_router(login.router)



