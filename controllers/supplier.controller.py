from sqlalchemy.orm import Session
from models.supplier import Supplier
from sqlalchemy import select

class SupplierController:

    @staticmethod
    def create(session: Session, name: str, email: str) -> Supplier:
        supplier = Supplier(name=name, email=email)
        session.add(supplier)
        session.flush()
        return supplier
    

    @staticmethod
    def get(session: Session, supplier_id: int) -> Supplier | None:
        return session.get(Supplier, supplier_id)


    @staticmethod
    def list_all(session: Session) -> list[Supplier]:
        stmt = select(Supplier)
        return session.execute(stmt).scalars().all()


    @staticmethod
    def update(session: Session, supplier_id: int, name: str | None = None, email: str | None = None) -> Supplier:
        supplier = session.get(Supplier, supplier_id)
        if not supplier:
            raise ValueError(f"Fournisseur introuvable : id={supplier_id}")
        if name is not None:
            supplier.name = name
        if email is not None:
            supplier.email = email
        return supplier


    @staticmethod
    def delete(session: Session, supplier_id: int) -> None:
        supplier = session.get(Supplier, supplier_id)
        if not supplier:
            raise ValueError(f"Fournisseur introuvable : id={supplier_id}")
        session.delete(supplier)