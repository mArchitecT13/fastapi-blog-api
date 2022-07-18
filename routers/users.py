from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from models import User
from database import get_db
from schemas import User as schemaUser, ShowUsers as schemaShowUsers
from hashing import Hash

router = APIRouter(
    tags=['users'],
    prefix="/users"
)

@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemaShowUsers)
def create(request: schemaUser ,db: Session=Depends(get_db)):

    hashed = Hash.bcrypt(request.password)
    new_user = User(name= request.name, email=request.email,password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("", status_code=status.HTTP_200_OK, response_model=List[schemaShowUsers])
def list(db: Session=Depends(get_db)):

    u = db.query(User).all()
    return u



@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemaShowUsers)
def user(id: int, db: Session=Depends(get_db)):
    b = db.query(User).filter(User.id==id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the {id} is not found in DB')
    return b