from fastapi import APIRouter, Depends, HTTPException, status
from db.schemas.items import ItemCreate, ShowItem
from db.models import Item, Admin, User
from datetime import datetime
from sqlalchemy.orm import Session
from db.database import get_db
from config.db_config import setting
from routers.login import oath2_scheme
from typing import List, Optional
from fastapi.encoders import jsonable_encoder
from jose import jwt


router = APIRouter()

def get_admin_from_token(db, token):
    ##using try block
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        # data is dictionary,
        # payload.get is a dictionary method to get data.
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify"
            )
        admin = db.query(Admin).filter(Admin.email == username).first()
        if admin is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email is not in our database"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify"
        )
    return admin

def get_user_from_token(db, token):
    ##using try block
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=setting.ALGORITHM)
        username = payload.get("sub")
        # data is dictionary,
        # payload.get is a dictionary method to get data.
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unable to verify"
            )
        user = db.query(User).filter(User.email == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="email is not in our database"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to verify"
        )
    return user


@router.post(
    "/create-an-item-backend",
    tags=["items"],
    response_model=ShowItem
)
def create_an_item(
        item: ItemCreate,
        db: Session = Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    admin = get_admin_from_token(db, token)
    # it only returns query
    if not admin:
        return {"Message": "please login as admin"}
    else:
        creation_date = datetime.now().date()

        item = Item(
            **item.dict(),
            creation_date=creation_date
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item



##doing search function for navbar
@router.get("/item/autocomplete")
def autocomplete(term: Optional[str] = None, db: Session = Depends(get_db)):
    #we`ll pull ^^^^ frm search 2 vvvvvvvvvvvvvvvvvvvv  and search
    items = db.query(Item).filter(Item.title.contains(term)).all()
    ##pull title from^^^^Item and fetch all item that match
    suggestions = []
    ##^^^ sug to show results in search
    for item in items:
        suggestions.append(item.title)
    return suggestions

@router.get("/item/all", tags=["items"], response_model=List[ShowItem])
    #show item matra rakhda error aayo,
    #so, added List
def retrieve_all_items(db: Session=Depends(get_db)):
    items = db.query(Item).all()
    return items


@router.get("/item/{id}", tags=["items"])
def retrieve_item_by_id(id, db: Session = Depends(get_db)):
        #get_db as we need to retrieve id from the database
    item = db.query(Item).filter(Item.id==id).first()
        #filter to filter whatever
        #.first to return first item
    if not item:    ##if item is null
        raise HTTPException(status_code=404, detail=f"Item {id} does not exist")
    return item


#using jsonable encoder
@router.put("/item/update/{id}", tags=["items"])
def update_item_by_id(
        id:int,
        item:ItemCreate,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    admin = get_admin_from_token(db, token)
    if not admin:
        return {"Message": "please login as admin"}
    else:
        existing_item = db.query(Item).filter(Item.id==id)
            #it only returns query
        if not existing_item.first():
                #.first() to fetch details
            return {"Message": f"Item ID {id} has no details "}
        if existing_item.first().id == admin.id:
            existing_item.update(jsonable_encoder(item))
            db.commit()
            return {"message": "details Successfully Updated"}
        else:
            return {"message": "you aren`t authorized"}


@router.delete("/item/delete/{id}", tags=["items"])
def delete_item_by_id(
        id:int,
        db:Session=Depends(get_db),
        token:str=Depends(oath2_scheme)
):
    user = get_user_from_token(db, token)
    existing_item = db.query(Item).filter(Item.id == id)
        # it only returns query
    if not existing_item.first():
            #.first() to fetch details
        return {"message": f"Item ID {id} has no details "}
    if existing_item.first().id >0:
        existing_item.delete()
        db.commit()
        return {"message": f"Item id: {id} Successfully Deleted"}
    else:
        return {"message": "you aren`t authorized"}
