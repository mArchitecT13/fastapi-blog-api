
from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Blog
from database import get_db
from schemas import ShowBlog as schemaShowBlog, Blog as schemaBlog, User as schemaUser
from oauth2 import get_current_user



router = APIRouter(
    tags=['blogs'],
    prefix="/blog"
)

@router.get("", status_code=status.HTTP_200_OK, response_model=List[schemaShowBlog])
def all(db: Session=Depends(get_db), current_user: schemaUser=Depends(get_current_user) ):

    blogs = db.query(Blog).all()
    return blogs



@router.post("", status_code=status.HTTP_201_CREATED)
def create(Request: schemaBlog, db: Session=Depends(get_db), current_user: schemaUser=Depends(get_current_user)):

    new_blog = Blog(title= Request.title, description=Request.description)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemaShowBlog)
def blog(id: int, db: Session=Depends(get_db), current_user: schemaUser=Depends(get_current_user)):
    b = db.query(Blog).filter(Blog.id==id).first()
    if not b:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'the {id} is not found in DB')
    return b


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, tags=['blogs'])
def update(id: int, request: schemaBlog, db: Session=Depends(get_db), current_user: schemaUser=Depends(get_current_user)):
    b = db.query(Blog).filter(Blog.id==id)

    if not b.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
    
    b.update(request.dict())
    db.commit()

    return {'details': 'updated'}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session=Depends(get_db), current_user: schemaUser=Depends(get_current_user)):
    b = db.query(Blog).filter(Blog.id==id)

    if not b.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'{id} not found')
    
    b.delete(synchronize_session=False)
    db.commit()

    return {'details': 'deleted'}