from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends
from database.db import SessionLocal
from controllers.category_controller import CategoryController

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class CategoryCreate(BaseModel):
    name: str

class CategoryUpdate(BaseModel):
    name: str

@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    categories = CategoryController.list_all(db)
    return [{"id": c.id, "name": c.name} for c in categories]

@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = CategoryController.get(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="categorie introuvable")
    return {"id": category.id, "name": category.name}

@router.post("/", status_code=201)
def create_category(data: CategoryCreate, db: Session = Depends(get_db)):
    category = CategoryController.create(db, name=data.name)
    db.commit()
    return {"id": category.id, "name": category.name}

@router.put("/{category_id}")
def update_category(category_id: int, data: CategoryUpdate, db: Session = Depends(get_db)):
    try:
        category = CategoryController.update(db, category_id, name=data.name)
        db.commit()
        return {"id": category.id, "name": category.name}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    try:
        CategoryController.delete(db, category_id)
        db.commit()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    