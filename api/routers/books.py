from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.book_controller import BookController

router = APIRouter(prefix="/books", tags=["Books"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class BookCreate(BaseModel):
    title: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    author_id: int
    supplier_id: int
    category_ids: list[int] | None=None

class BookUpdate(BaseModel):
    price: float = Field(..., gt=0)

@router.get("/")
def list_books(db: Session = Depends(get_db)):
    books = BookController.list_all(db)
    return [{"id": b.id, "title": b.title, "price": b.price, "stock_quantity": b.stock_quantity} for b in books]

@router.get("/{book_id}")
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = BookController.get(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return {"id": book.id, "title": book.title}

@router.post("/", status_code=201)
def create_book(data: BookCreate, db: Session = Depends(get_db)):
    book = BookController.create(
        db, title=data.title, price=data.price, stock=data.stock,
        author_id=data.author_id, supplier_id=data.supplier_id, 
        category_ids=data.category_ids)
    db.commit()
    return {"id": book.id, "name": book.title}

@router.put("/{book_id}")
def update_book(book_id: int, data: BookUpdate, db: Session = Depends(get_db)):
    try:
        book = BookController.update_price(db, book_id, new_price=data.price)
        db.commit()
        return {"id": book.id, "title": book.title}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    try:
        BookController.delete(db, book_id)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))