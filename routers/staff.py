from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.schemas import StaffCreate, ShowStaff
from db.database import get_db
from config.hashing import Hasher
from db.models import Staff

router=APIRouter()


@router.post(
    "/staff",
    tags=['staff'],
    response_model=ShowStaff
)
def create_staff(
        staff: StaffCreate,
        db: Session = Depends(get_db)
):
    staff = Staff(
        email=staff.email,
        password=Hasher.get_hash_password(staff.password),
        #user_id=staff.staff_id
    )
    db.add(staff)
    db.commit()
    db.refresh(staff)
    return staff


@router.get("/staff/{id}", tags=["staff"])
def retrieve_staff_by_id(id, db: Session = Depends(get_db)):
    admin = db.query(Staff).filter(Staff.id==id).first()
    if not admin:
        raise HTTPException(status_code=404, detail=f"Admin {id} does not exist")
    return admin
