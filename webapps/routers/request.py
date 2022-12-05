from fastapi import APIRouter, Request, Response, Depends
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_db

router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/request_item")
def request_item(request: Request):
    return templates.TemplateResponse(
        "request_item.html",
        {"request": request}
    )


#@router.post("/request_item")
#async def request(
#        response: Response,
#        request: Request,
#        db: Session = Depends(get_db)
#):
#    form = await request.form()
#   title = form.get("item")