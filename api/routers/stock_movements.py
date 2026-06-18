from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.stock_movement_controller import StockMovementController

router = APIRouter(prefix="/stock-movements", tags=["Stock Movements"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def list_stock_movements(db: Session = Depends(get_db)):
    stock_movements = StockMovementController.list_all(db)
    return [{"id": s.id, "book_id": s.book_id, "quantity": s.quantity, "reason": s.reason.value, "date": s.date} for s in stock_movements]

@router.get("/book/{book_id}")
def book_stock_movements(book_id: int, db: Session = Depends(get_db)):
    stock_movements = StockMovementController.list_by_book(db, book_id)
    if not stock_movements:
        raise HTTPException(status_code=404, detail="Pas de changement de stock pour ce livre")
    return [{"id": s.id, "book_id": s.book_id, "quantity": s.quantity, "reason": s.reason.value, "date": s.date} for s in stock_movements]
