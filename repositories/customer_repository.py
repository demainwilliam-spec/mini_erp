from sqlalchemy import select
from sqlalchemy.orm import Session
from models.customer import Customer


class CustomerRepository:

    @staticmethod
    def add(session: Session, customer: Customer) -> Customer:
        session.add(customer)
        session.flush()
        return customer

    @staticmethod
    def get_by_id(session: Session, customer_id: int) -> Customer | None:
        return session.get(Customer, customer_id)

    @staticmethod
    def get_all(session: Session) -> list[Customer]:
        stmt = select(Customer)
        return session.execute(stmt).scalars().all()

    @staticmethod
    def delete(session: Session, customer: Customer) -> None:
        session.delete(customer)

