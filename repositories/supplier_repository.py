from sqlalchemy import select
from sqlalchemy.orm import Session
from models.supplier import Supplier


class SupplierRepository:

    @staticmethod
    def add(session: Session, supplier: Supplier) -> Supplier:
        session.add(supplier)
        session.flush()
        return supplier

    @staticmethod
    def get_by_id(session: Session, supplier_id: int) -> Supplier | None:
        return session.get(Supplier, supplier_id)

    @staticmethod
    def get_all(session: Session) -> list[Supplier]:
        stmt = select(Supplier)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, supplier: Supplier) -> None:
        session.delete(supplier)