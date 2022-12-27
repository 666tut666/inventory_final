import datetime
from typing import Optional
from fastapi import APIRouter, Request, Depends, status, HTTPException #, responses
from fastapi.templating import Jinja2Templates
from fastapi.encoders import jsonable_encoder
from routers.login import oath2_scheme
from db.models import Item, User, Admin
from sqlalchemy.orm import Session
from db.database import get_db
from jose import jwt
from config.db_config import setting
from db.schemas.items import ItemCreate, ShowItem

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")
    #defined path where html files are
        ##templates.....


def get_user_from_token(db, token):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, setting.ALGORITHM)
        username = payload.get("sub")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate Credentials",
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate Credentials",
        )
    user = db.query(User).filter(User.email == username).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    return user
@router.get("/")
def item_home(
        request: Request,
        db:Session=Depends(get_db),
        msg:str=None
):
    items = db.query(Item).all()
    return templates.TemplateResponse("item_hp.html", {"request": request, "items": items, "msg": msg})
        #using pydantic approach
        ##taking i/p: as request// request type
            #item_hp.html is item`s home page
            ##gotta declare Request in Jinja
        ## as we have used item_hp, gotta define it there too

#updating item
@router.get("/item/update/{id}", tags=["item"])
def update_item_by_id(
    id: int,
    request:Request,
    db:Session=Depends(get_db)
):
    item = db.query(Item).filter(Item.id==id).first()
    return templates.TemplateResponse(
        "update_item.html",
        {
            "request":request,
            "item":item
        }
    )


@router.get("/detail/{id}")
def item_detail(
        request: Request,
        id: int,
        db: Session = Depends(get_db)
):
    item = db.query(Item).filter(Item.id==id).first()
    user = db.query(User).filter(User.id==Admin.user_id).first()
    return templates.TemplateResponse(
        "item_detail.html",
        {
            "request": request,
            "item": item,
            "user": user
        }
    )


@router.get("/create-an-item")
def create_an_item(
        request: Request
):
    return templates.TemplateResponse(
        "create_item.html",
        {"request": request}
    )


#using post method for submit button
#gotta read data so async
@router.post("/create-an-item")
async def create_an_item(
        request: Request,
        db: Session = Depends(get_db)
):


    form = await request.form()
    #id = Optional[form.get("id")]
    title = form.get("title")
    item_type = form.get("item_type")
    category = form.get("category")
    quantity = form.get("quantity")
    creation_date = form.get("creation_date")



    errors = []
        #we need to define error dictionary
        #it`ll store errors
    if not title or len(title) < 2:
        errors.append("Title should be greater than two character")
    if not item_type or len(item_type) < 3:
        errors.append("type should be be more than three characters")
    if not quantity:
        errors.append("Quantity should be be more than three characters")
    if not category or len(category) < 3:
        errors.append("Category should be be more than three characters")



    #reload page showing what error, SO
    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_item.html",
            {
                "request": request,
                "errors": errors
            }
        )
    #{....} passing context dict, request and showing error

    try:
        token = request.cookies.get("access_token")
        if not token:
            errors.append("Please Login first")
            return templates.TemplateResponse(
                "login.html",
                {
                    "request":request,
                    "errors":errors
                }
            )
        scheme, _, param = token.partition(" ")
        payload = jwt.decode(param, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        email = payload.get("sub")
        if email is None:
            errors.append("Kindly login first, you are not authenticated")
            return templates.TemplateResponse(
                "login.html", {"request": request, "errors": errors}
            )
        else:
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

                return templates.TemplateResponse(
                    "item_added.html",
                    {
                        "request": request
                    }
                )

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

@router.get("/update-delete-item")
def items_to_delete(
        request:Request,
        db:Session=Depends(get_db)
):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("please login as admin")
        return templates.TemplateResponse(
            "update_delete_item.html",
            {
                "request": request,
                "errors": errors
            }
        )

    else:
        try:
            scheme, _, param = token.partition(" ")
            payload = jwt.decode(
                param, setting.SECRET_KEY, algorithms=setting.ALGORITHM
            )
            email = payload.get("sub")
            print(email)
            admin = db.query(Admin).filter(Admin.email == email).first()
            items = db.query(Item).all()
            return templates.TemplateResponse(
                "update_delete_item.html", {"request": request, "items": items}
            )
        except Exception as e:
            print(e)
            errors.append("You are not Authenticated")
            return templates.TemplateResponse(
                "update_delete_item.html",
                {"request": request, "errors": errors},
            )





@router.get("/request-item")
def request_item(request: Request):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("please login")
        return templates.TemplateResponse(
            "request_item.html",
            {
                "request": request,
                "errors": errors
            }
        )
    return templates.TemplateResponse(
        "request_item.html",
        {"request": request}
    )

@router.put("/item/update/{id}", tags=["item"])
def update_an_item(
        request: Request,
        id: int,
        db: Session = Depends(get_db)
):
    errors = []
    token = request.cookies.get("access_token")
    if token is None:
        errors.append("please login as admin")
        return templates.TemplateResponse(
            "update_item.html",
            {
                "request": request,
                "errors": errors
            }
        )
    else:
        try:
            existing_item = db.query(Item).filter(Item.id == id)
            # it only returns query
            if not existing_item.first():
                # .first() to fetch details
                return {"Message": f"Item ID {id} has no details "}
            if existing_item.first().id > 0:
                existing_item.update(jsonable_encoder(item))

                db.commit()

            return templates.TemplateResponse(
                "update_delete_item.html", {"request": request, "items": items}
            )
        except Exception as e:
            print(e)
            errors.append("You are not Authenticated")
            return templates.TemplateResponse(
                "update_delete_item.html",
                {"request": request, "errors": errors},
            )


@router.post("/request-item/{id}",tags=["items"])
def request_item(
        request: Request,
        id: int,
        db: Session = Depends(get_db)
):
    scheme, _, param = token.partition(" ")
    payload = jwt.decode(
        param, setting.SECRET_KEY, algorithms=setting.ALGORITHM
    )
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


@router.get("/search")
def search_jobs(request: Request, query: Optional[str], db: Session = Depends(get_db)):
    items = db.query(Item).filter(Item.title.contains(query)).all()
    return templates.TemplateResponse(
        "item_hp.html", {"request": request, "items": items}
    )