from database.db import init_db
from models.author import Author
from models.supplier import Supplier
from models.category import Category
from models.book import Book
from models.customer import Customer
from models.order import Order, OrderLine


init_db()
print("Tables créées !")