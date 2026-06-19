
from sqlalchemy.orm import Session
from models.stock_movement import StockMovement
from repositories.stock_movement_repository import StockMovementRepository


class StockMovementController:

    @staticmethod
    def list_all(session: Session) -> list[StockMovement]:
        return StockMovementRepository.get_all(session)

    @staticmethod
    def list_by_book(session: Session, book_id: int) -> list[StockMovement]:
        return StockMovementRepository.get_by_book(session, book_id)