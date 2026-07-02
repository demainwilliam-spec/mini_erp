from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.customer_controller import CustomerController

router = APIRouter(prefix="/customers", tags=["Customers"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CustomerCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr

class CustomerUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


@router.get("/")
def list_customers(db: Session = Depends(get_db)):
    customers = CustomerController.list_all(db)
    return [{"id": c.id, "name": c.name, "email": c.email} for c in customers]


@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = CustomerController.get(db, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Client introuvable")
    return {"id": customer.id, "name": customer.name}

@router.post("/", status_code=201)
def create_customer(data: CustomerCreate, db: Session = Depends(get_db)):
    customer = CustomerController.create(db, name=data.name, email=data.email)
    db.commit()
    return {"id": customer.id, "name": customer.name}


@router.put("/{customer_id}")
def update_customer(customer_id: int, data: CustomerUpdate, db: Session = Depends(get_db)):
    try:
        customer = CustomerController.update(db, customer_id, name=data.name, email=data.email)
        db.commit()
        return {"id": customer.id, "name": customer.name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    try:
        CustomerController.delete(db, customer_id)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))