import datetime

from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.encoders import jsonable_encoder
from fastapi.templating import Jinja2Templates
from db.models import Item, User, Admin
from sqlalchemy.orm import Session
from db.database import get_db
from jose import jwt
from config.db_config import setting

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/pending")
def create_an_item(
        request: Request
):
    return templates.TemplateResponse(
        "pending.html",
        {"request": request}
    )
@router.post("/create-an-item")
async def create_an_item(
        request: Request,
        db: Session = Depends(get_db)
):
       try:
        token = request.cookies.get("access_token")
        if token is None:
            errors.append("Please Login first")
            return templates.TemplateResponse(
                "login.html",
                {
                    "request":request,
                    "errors":errors
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
            admin = db.query(Admin).filter(Admin.email==email).first()
            if admin is None:
                errors.append("You aren`t authenticated, Please login")
                return templates.TemplateResponse(
                    "create_item.html",
                    {
                        "request":request,
                        "errors":errors
                    }
                )
            else:
                #if admin is not none
                #admin exists and is logged in
                item = Item(
                    title=title,
                    item_type=item_type,
                    category=category,
                    quantity=quantity,
                    creation_date=datetime.date.today(),

                )
                db.add(item)
                db.commit()
                db.refresh(item)
                return responses.RedirectResponse(
                    f"/detail/{item.id}",
                    status_code=status.HTTP_302_FOUND
                )
    except Exception as e:
        print(e)


def update_item_by_id(
        id:int,
        item:ItemCreate,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id==id)
        #it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"Message": f"Item ID {id} has no details "}
    if existing_item.first().owner_id == user.id:
        existing_item.update(jsonable_encoder(item))
        db.commit()
        return {"message": f"details for {id} Successfully Updated"}
    else:
        return {"message": "you aren`t authorized"}