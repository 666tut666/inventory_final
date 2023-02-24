from fastapi import APIRouter, Request, Depends, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Admin, User
from config.hashing import Hasher
from jose import jwt
from config.db_config import setting

# as config.py has ALGORITHM, SECRET_KEY defined in Settings class


router = APIRouter(include_in_schema=False)
templates = Jinja2Templates(directory="templates")


@router.get("/login")
def login(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )


@router.post("/login")
async def login(
        response: Response,
        request: Request,
        db: Session = Depends(get_db)
):
    form = await request.form()
    email = form.get("email")
    password = form.get("password")
    errors = []
    if not email:
        errors.append("please enter valid email")
    if not password or len(password) < 5:
        errors.append("Password must be more than 5 characters")

    try:
        # checking if email exists on db.
        admin = db.query(Admin).filter(Admin.email == email).first()
        user = db.query(User).filter(User.email == email).first()
        if admin is None:
            errors.append("Email does not exist")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "errors": errors}
            )
        if user is None:
            print("hello")
            errors.append("Email does not exist")
            return templates.TemplateResponse(
                "login.html",
                {"request": request, "errors": errors}
            )

            # returning login page again as
            # login was not successful
        else:
            if Hasher.verify_password(password, admin.password):
                # password is plain password,
                # admin.password is hashed pw from db
                # after password is verified, need jwt token, so
                data = {"sub": email}
                # jwt.io remember?

                jwt_token = jwt.encode(
                    data,
                    setting.SECRET_KEY,
                    algorithm=setting.ALGORITHM
                )
                # we aren`t using OAth2 of swagger UI authorization
                # we are using our own login form,
                # we are now using cookie to store password
                msg = "Login Success"
                response = templates.TemplateResponse(
                    "login.html",
                    {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token",
                    value=f"Bearer {jwt_token}",
                    httponly=True
                )
                return response
                # value is Bearer <token>
                # using Http only = True - notes ma explained cha

            if Hasher.verify_password(password, admin.password):
                data = {"sub": email}

                jwt_token = jwt.encode(
                    data,
                    setting.SECRET_KEY,
                    algorithm=setting.ALGORITHM
                )

                msg = "Login Success"
                response = templates.TemplateResponse(
                    "login.html",
                    {"request": request, "msg": msg}
                )
                response.set_cookie(
                    key="access_token",
                    value=f"Bearer {jwt_token}",
                    httponly=True
                )
                return response



            else:
                errors.append("Invalid Password")
                return templates.TemplateResponse(
                    "login.html",
                    {"request": request, "errors": errors}
                )
    except Exception as e:
        print(e)
    #except:
    #    errors.append("something`s wrong")
    #    return templates.TemplateResponse(
    #        "login.html",
    #        {"request": request, "errors": errors}
    #    )