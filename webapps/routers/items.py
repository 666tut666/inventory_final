import datetime

from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from db.models import Item, User, Admin
from sqlalchemy.orm import Session
from db.database import get_db
from jose import jwt
from config.db_config import setting

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")
    #defined path where html files are
        ##templates.....


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
        errors.append("type should be be more than tree characters")
    if not quantity:
        errors.append("Quantity should be be more than tree characters")
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

@router.get("/pending")
def create_an_item(
        request: Request
):
    return templates.TemplateResponse(
        "pending.html",
        {"request": request}
    )

