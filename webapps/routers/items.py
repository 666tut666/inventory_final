from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from db.models import Item, User, Admin
from sqlalchemy.orm import Session
from db.database import get_db

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
def create_an_item(request: Request):
    return templates.TemplateResponse(
        "create_item.html",
        {"request": request}
    )


#using post method for submit button
#gotta read data so async
@router.post("/create-an-item")
async def create_an_item(request: Request):
    form = await request.form()
    title = form.get("title")
    description = form.get("description")
    errors = []
        #we need to define error dictionary
        #it`ll store errors
    if not title or len(title) < 2:
        errors.append("Title should be greater than two character")
    if not description or len(description) <10:
        errors.append("Description should be be more than ten characters")
    #if there are errors len will not be 0
    #in case of error we gotta display error
    #and also reload page showing what error, SO
    if len(errors) > 0:
        return templates.TemplateResponse(
            "create_item.html",
            {
                "request": request,
                "errors": errors
            }
        )
    #{....} passing context dict, request and showing error
