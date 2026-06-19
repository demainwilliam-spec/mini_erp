from sqlalchemy import select
from sqlalchemy.orm import Session
from models.stock_movement import StockMovement


class StockMovementRepository:

    @staticmethod
    def add(session: Session, movement: StockMovement) -> StockMovement:
        session.add(movement)
        return movement

    @staticmethod
    def get_all(session: Session) -> list[StockMovement]:
        stmt = select(StockMovement).order_by(StockMovement.date.desc())
        return session.execute(stmt).scalars().all()

    @staticmethod
    def get_by_book(session: Session, book_id: int) -> list[StockMovement]:
        stmt = (
            select(StockMovement)
            .where(StockMovement.book_id == book_id)
            .order_by(StockMovement.date.desc())
        )
        return session.execute(stmt).scalars().all()