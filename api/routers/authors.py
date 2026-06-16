from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.author_controller import AuthorController

router = APIRouter(prefix="/authors", tags=["Authors"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class AuthorCreate(BaseModel):
    name: str


class AuthorUpdate(BaseModel):
    name: str

@router.get("/")
def list_authors(db: Session = Depends(get_db)):
    authors = AuthorController.list_all(db)
    return [{"id": a.id, "name": a.name} for a in authors]


@router.get("/{author_id}")
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = AuthorController.get(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Auteur introuvable")
    return {"id": author.id, "name": author.name}


@router.post("/", status_code=201)
def create_author(data: AuthorCreate, db: Session = Depends(get_db)):
    author = AuthorController.create(db, name=data.name)
    db.commit()
    return {"id": author.id, "name": author.name}


@router.put("/{author_id}")
def update_author(author_id: int, data: AuthorUpdate, db: Session = Depends(get_db)):
    try:
        author = AuthorController.update(db, author_id, name=data.name)
        db.commit()
        return {"id": author.id, "name": author.name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{author_id}", status_code=204)
def delete_author(author_id: int, db: Session = Depends(get_db)):
    try:
        AuthorController.delete(db, author_id)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))