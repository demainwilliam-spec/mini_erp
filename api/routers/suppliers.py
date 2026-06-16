from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.supplier_controller import SupplierController

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class SupplierCreate(BaseModel):
    name: str
    email: str

class SupplierUpdate(BaseModel):
    name: str
    email: str

@router.get("/")
def list_suppliers(db: Session = Depends(get_db)):
    suppliers = SupplierController.list_all(db)
    return [{"id": s.id, "name": s.name, "email": s.email} for s in suppliers]

@router.get("/{supplier_id}")
def get_supplier(supplier_id: int, db: Session = Depends(get_db)):
    supplier = SupplierController.get(db, supplier_id)
    if not supplier:
        raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    return {"id": supplier.id, "name": supplier.name, "email": supplier.email}

@router.post("/", status_code=201)
def create_supplier(data: SupplierCreate, db: Session = Depends(get_db)):  
    supplier = SupplierController.create(db, name=data.name, email=data.email)
    db.commit()
    return {"id": supplier.id, "name": supplier.name, "email": supplier.email}

@router.put("/{supplier_id}")
def update_supplier(supplier_id: int, data: SupplierUpdate, db: Session = Depends(get_db)):
    try:
        supplier = SupplierController.update(db, supplier_id, name=data.name, email=data.email)
        db.commit()
        return {"id": supplier.id, "name": supplier.name, "email": supplier.email}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{supplier_id}", status_code=204)
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    try:
        SupplierController.delete(db, supplier_id)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
