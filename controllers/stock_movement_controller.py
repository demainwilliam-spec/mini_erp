from sqlalchemy import select
from sqlalchemy.orm import Session

from models.stock_movement import StockMovement

class StockMovementController:

    @staticmethod
    def list_all(session: Session) -> list[StockMovement]:
        stmt = select(StockMovement).order_by(StockMovement.date.desc())
        return session.execute(stmt).scalars().all()
    
    @staticmethod
    def list_by_book(session: Session, book_id: int) -> list[StockMovement]:
        stmt = select(StockMovement).where(StockMovement.book_id == book_id).order_by(StockMovement.date.desc())
        return session.execute(stmt).scalars().all()
    