from database.db import init_db
from models.author import Author
from models.supplier import Supplier
from models.category import Category
from models.book import Book

init_db()
print("Tables créées !")