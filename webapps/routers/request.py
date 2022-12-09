from fastapi import APIRouter, Request, responses, Depends, status
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Item
from sqlalchemy.exc import IntegrityError
from config.db_config import setting
import psycopg2


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/request_item")
def request_item(request: Request):
    return templates.TemplateResponse(
        "request_item.html",
        {"request": request}
    )


@router.post("/request_item/{id}")
def request_item():
    conn = psycopg2.connect(
        database=setting.POSTGRES_DATABASE,
        user=setting.POSTGRES_USER,
        password=setting.POSTGRES_PASSWORD,
        host='127.0.0.1',
        port=setting.POSTGRES_PORT
    )
    conn.autocommit=True

    cursor = conn.cursor()

    sql = '''SELECT * from ITEMS'''
    cursor.execute(sql)
    print(cursor.fetchall())

    sql = "UPDATE ITEMS SET QUANTITY = QUANTITY -1"
    cursor.execute(sql)
    conn.commit()
    conn.close()