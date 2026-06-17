from fastapi import FastAPI
from database.db import SessionLocal
from api.routers import authors, suppliers, categories, books, customers, orders, stock_movements
from models import author, supplier, category, book, customer, order, stock_movement

app = FastAPI(
    title="Mini ERP API",
    description="API REST pour le mini ERP",
    version="1.0.0"
)

app.include_router(authors.router)
app.include_router(suppliers.router)
app.include_router(categories.router)
app.include_router(books.router)
# app.include_router(customers.router)
# app.include_router(orders.router)
# app.include_router(stock_movements.router)
@app.get("/")
def root():
    return {"message": "Bienvenue sur le Mini ERP API !"}