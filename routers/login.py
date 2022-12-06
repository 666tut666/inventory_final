from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db.models import Admin
from config.hashing import Hasher
from jose import jwt
from config.db_config import setting

oath2_scheme = OAuth2PasswordBearer(tokenUrl='/login/token')
# Oath2 session created
# tokenUrl to give route for the token

router = APIRouter()


@router.post(
    "/login/token",
    tags=["login"]
)
def retrieve_token_after_authentication(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db:Session = Depends(get_db)
):
    ##as form data depends on the form itself, nothing passed in form data's Depends
    ##but the database session "db:Session", Depends on get_db
    admin = db.query(Admin).filter(Admin.email==form_data.username).first()
        #checking if the table has provided email
    if not admin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Username"
        )
    ##we have set password related code in hashing.py
    ##in models.py class Admin,
        ##password Column is already defined
    #Hasher in hashing.py we have verify_password
    #so calling it
    if not Hasher.verify_password(form_data.password, admin.password):
        ##in hasher.py's verify_password
            # we have: return pwd_context.verify(plain_password, hash_password)
            #so using similar approach

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Password"
        )
    data = {"sub": form_data.username}
        #data should be dictionary
        #we are using sub now
            ##as sub is unique key so is our username(which is email)
    jwt_token = jwt.encode(data, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
        #pulling SECURITY_KEY, ALGORITHM from config
    return {"access_token": jwt_token, "token_type": "bearer"}
        #bearer as our token holds actual data
