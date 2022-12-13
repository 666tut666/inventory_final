from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Item, User
from config.db_config import setting
import psycopg2
from jose import jwt


router = APIRouter(include_in_schema=False  )
templates = Jinja2Templates(directory="templates")


@router.get("/request_item/{id}",tags=["items"])
def request_item(request: Request):
    return templates.TemplateResponse(
        "request_item.html",
        {"request": request}
    )


@router.post("/request_item/{id}",tags=["items"])
def request_item(
        request: Request,
        id: int,
        db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id==id).first
    user = db.query(User).filter(User.email == email).first()
    errors = []
    if not user:
        errors.append("Please login")

    email = payload.get("sub")

    if user is None:
        errors.append("You aren`t authenticated, Please login")
        return templates.TemplateResponse(
            "create_item.html",
            {
                "request": request,
                "errors": errors
            }
        )
    else:
        try:
            token = request.cookies.get("access_token")
            if token is None:
                errors.append("Please Login first")
                return templates.TemplateResponse(
                    "login.html",
                    {
                        "request": request,
                        "errors": errors
                    }
                )
            else:
                scheme, _, param = token.partition(" ")
                payload = jwt.decode(
                    param,
                    setting.SECRET_KEY,
                    algorithms=setting.ALGORITHM
                )
                email = payload.get("sub")
                admin = db.query(Admin).filter(Admin.email == email).first()
                if admin is None:
                    errors.append("You aren`t authenticated, Please login")
                    return templates.TemplateResponse(
                        "create_item.html",
                        {
                            "request": request,
                            "errors": errors
                        }
                    )
                else:
                    # if admin is not none
                    # admin exists and is logged in
                    conn = psycopg2.connect(
                        database=setting.POSTGRES_DATABASE,
                        user=setting.POSTGRES_USER,
                        password=setting.POSTGRES_PASSWORD,
                        host='127.0.0.1',
                        port=setting.POSTGRES_PORT
                    )
                    conn.autocommit = True

                    cursor = conn.cursor()

                    sql = '''SELECT * from ITEMS'''
                    cursor.execute(sql)
                    print(cursor.fetchall())

                    sql = "UPDATE ITEMS SET QUANTITY = QUANTITY -1"
                    cursor.execute(sql)
                    conn.commit()
                    conn.close()
        except Exception as e:
            print(e)
@router.get("/pending")
def create_an_item(
        request: Request
):
    return templates.TemplateResponse(
        "pending.html",
        {"request": request}
    )
