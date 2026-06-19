
from sqlalchemy.orm import Session
from models.customer import Customer
from repositories.customer_repository import CustomerRepository


class CustomerController:

    @staticmethod
    def create(session: Session, name: str, email: str) -> Customer:
        customer = Customer(name=name, email=email)
        return CustomerRepository.add(session, customer)

    @staticmethod
    def get(session: Session, customer_id: int) -> Customer | None:
        return CustomerRepository.get_by_id(session, customer_id)

    @staticmethod
    def list_all(session: Session) -> list[Customer]:
        return CustomerRepository.get_all(session)

    @staticmethod
    def update(session: Session, customer_id: int, name: str | None = None, email: str | None = None) -> Customer:
        customer = CustomerRepository.get_by_id(session, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        if name is not None:
            customer.name = name
        if email is not None:
            customer.email = email
        return customer

    @staticmethod
    def delete(session: Session, customer_id: int) -> None:
        customer = CustomerRepository.get_by_id(session, customer_id)
        if not customer:
            raise ValueError(f"Client introuvable : id={customer_id}")
        CustomerRepository.delete(session, customer)
