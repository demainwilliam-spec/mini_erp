from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.order_controller import OrderController
from sqlalchemy import select
from models.order import Order

router = APIRouter(prefix="/orders", tags=["Orders"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class OrderCreate(BaseModel):
    customer_id: int


class OrderLineAdd(BaseModel):
    book_id: int
    quantity: int


@router.get("/")
def list_orders(db: Session = Depends(get_db)):

    orders = db.execute(select(Order)).scalars().all()
    return [{"id": o.id, "status": o.status.value, "customer_id": o.customer_id} for o in orders]


@router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        return {"id": order.id, "status": order.status.value, "customer_id": order.customer_id}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/", status_code=201)
def create_order(data: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = OrderController.create_draft(db, customer_id=data.customer_id)
        db.commit()
        return {"id": order.id, "status": order.status.value}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{order_id}/add-line", status_code=201)
def add_line(order_id: int, data: OrderLineAdd, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        line = OrderController.add_line(db, order, book_id=data.book_id, quantity=data.quantity)
        db.commit()
        return {"id": line.id, "book_id": line.book_id, "quantity": line.quantity, "unit_price": float(line.unit_price)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/confirm")
def confirm_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        OrderController.confirm(db, order)
        db.commit()
        return {"id": order.id, "status": order.status.value}
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{order_id}/close")
def close_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        OrderController.close(db, order)
        db.commit()
        return {"id": order.id, "status": order.status.value}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{order_id}/summary")
def get_summary(order_id: int, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        return OrderController.summary(order)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, db: Session = Depends(get_db)):
    try:
        order = OrderController.get(db, order_id)
        db.delete(order)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))