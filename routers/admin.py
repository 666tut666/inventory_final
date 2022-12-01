from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas import AdminCreate, ShowAdmin
from database import get_db
from hashing import Hasher
from models import Admin, User, AdminType
from typing import List

router=APIRouter()


@router.post(
    "/admin",
    tags=['admin'],
    response_model=ShowAdmin
)
def create_admin(
        admin: AdminCreate,
        db: Session = Depends(get_db)
):
    admin = Admin(
        email=admin.email,
        password=Hasher.get_hash_password(admin.password),
        user_id=admin.admin_id
        #admin_type_id=admin.admin_type_id
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
