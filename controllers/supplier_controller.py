
from sqlalchemy.orm import Session
from models.supplier import Supplier
from repositories.supplier_repository import SupplierRepository


class SupplierController:

    @staticmethod
    def create(session: Session, name: str, email: str) -> Supplier:
        supplier = Supplier(name=name, email=email)
        return SupplierRepository.add(session, supplier)

    @staticmethod
    def get(session: Session, supplier_id: int) -> Supplier | None:
        return SupplierRepository.get_by_id(session, supplier_id)

    @staticmethod
    def list_all(session: Session) -> list[Supplier]:
        return SupplierRepository.get_all(session)

    @staticmethod
    def update(session: Session, supplier_id: int, name: str, email: str) -> Supplier:
        supplier = SupplierRepository.get_by_id(session, supplier_id)
        if not supplier:
            raise ValueError(f"Fournisseur introuvable : id={supplier_id}")
        supplier.name = name
        supplier.email = email
        return supplier

    @staticmethod
    def delete(session: Session, supplier_id: int) -> None:
        supplier = SupplierRepository.get_by_id(session, supplier_id)
        if not supplier:
            raise ValueError(f"Fournisseur introuvable : id={supplier_id}")
        SupplierRepository.delete(session, supplier)