from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.schemas.admin import AdminCreate, ShowAdmin
from db.database import get_db
from config.hashing import Hasher
from db.models import Admin
from typing import List

router=APIRouter()

@router.get(
    "/admin",
    tags=['admin']
)
##tags=["..."] to manage kun tag ma halnae
def get_user():
    return {"message": "hello user"}



@router.post(
    "/admin",
    tags=['admin'],
    response_model= ShowAdmin
)
def register(
        admin: AdminCreate,
        db: Session = Depends(get_db)
):
    admin = Admin(
        email=admin.email,
        password=Hasher.get_hash_password(admin.password)
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


@router.get(
    "/admin/all",
    tags=['admin'],
    response_model=List[ShowAdmin]
)
def get_admin(
        db: Session = Depends(get_db)
):
    admins = db.query(Admin).all()
    return admins



@router.get("/admin/{id}", tags=["admin"])
def retrieve_admin_by_id(id, db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.id==id).first()
    if not admin:
        raise HTTPException(status_code=404, detail=f"Admin {id} does not exist")
    return admin
