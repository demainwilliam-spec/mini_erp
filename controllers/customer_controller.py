from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session
from models.customer import Customer


class CustomerController:

    @staticmethod
    def create(session: Session, name: str, email: str) -> Customer:
        customer = Customer(name=name, email=email)
        session.add(customer)
        session.flush()
        return customer
    
    @staticmethod
    def get(session: Session, customer_id: int) -> Customer:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        return customer

    @staticmethod
    def list_all(session: Session) -> list[Customer]:
        stmt = select(Customer)
        return session.execute(stmt).scalars().all()
    
    @staticmethod
    def update(session: Session, customer_id: int, name: str | None = None, email: str | None = None) -> Customer:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        return customer

    @staticmethod
    def delete(session: Session, customer_id: int) -> None:
        customer = session.get(Customer, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        session.delete(customer)