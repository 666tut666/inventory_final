from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from db.models import User
from config.hashing import Hasher
from sqlalchemy.orm import Session
from db.database import get_db
from sqlalchemy.exc import IntegrityError


router = APIRouter(include_in_schema=False)
    #include_in_schema=False
    #to remove routers as default
    #in    swagger UI
templates = Jinja2Templates(directory="templates")


@router.get("/register")
def registration(request: Request):
    return templates.TemplateResponse(
        "user_register.html",
        {"request": request}
    )


@router.post("/register")
##even if we have same link and function
##we are using post and get
##so it`s kk
async def registration(
        request: Request,
        db: Session = Depends(get_db)
):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
        #error is list for now
    if len(password) < 6:
        errors.append("password must be more than 6 characters")
        return templates.TemplateResponse(
            "user_register.html",
            {"request": request, "errors": errors}
        )
            #error aayae user_register.html reload huncha
    user = User(email=email, password=Hasher.get_hash_password(password))
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return responses.RedirectResponse(
            "/?msg=successfully registered",
            status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Email already exists")
        return templates.TemplateResponse(
            "user_register.html",
            {"request": request, "errors": errors}
        )
