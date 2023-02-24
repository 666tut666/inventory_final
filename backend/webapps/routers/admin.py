from fastapi import APIRouter, Request, Depends, responses, status
from fastapi.templating import Jinja2Templates
from db.models import Admin
from config.hashing import Hasher
from sqlalchemy.orm import Session
from db.database import get_db
from sqlalchemy.exc import IntegrityError


router = APIRouter(include_in_schema=False)
    #include_in_schema=False
    #to remove routers as default
templates = Jinja2Templates(directory="templates")


@router.get("/admin_register")
def registration(request: Request):
    return templates.TemplateResponse(
        "admin_register.html",
        {"request": request}
    )


@router.post("/admin_register")
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
            "admin_register.html",
            {"request": request, "errors": errors}
        )
            #error aayae admin_register.html reload huncha
    admin = Admin(email=email, password=Hasher.get_hash_password(password))

    try:
        db.add(admin)
        db.commit()
        db.refresh(admin)
        return responses.RedirectResponse(
            "/?msg=successfully registered",
            status_code=status.HTTP_302_FOUND
        )
    except IntegrityError:
        errors.append("Email already exists")
        return templates.TemplateResponse(
            "admin_register.html",
            {"request": request, "errors": errors}
        )
