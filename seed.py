from database.db import SessionLocal
from models.author import Author
from models.supplier import Supplier
from models.category import Category
from models.book import Book
from models.customer import Customer
from models.order import Order, OrderLine


def seed():
    session = SessionLocal()
    try:
        # Auteurs
        orwell = Author(name="George Orwell")
        herbert = Author(name="Frank Herbert")
        session.add_all([orwell, herbert])
        session.flush()

        # Fournisseurs
        supplier1 = Supplier(name="Librairie du Nord", email="contact@libnord.be")
        supplier2 = Supplier(name="Editions Sud", email="contact@edsud.be")
        session.add_all([supplier1, supplier2])
        session.flush()

        # Catégories
        sf = Category(name="Science-Fiction")
        pol = Category(name="Politique")
        roman = Category(name="Roman")
        session.add_all([sf, pol, roman])
        session.flush()

        # Livres
        book1 = Book(title="1984", price=14.99, stock_quantity=10, author_id=orwell.id, supplier_id=supplier1.id)
        book2 = Book(title="La Ferme des Animaux", price=9.99, stock_quantity=5, author_id=orwell.id, supplier_id=supplier1.id)
        book3 = Book(title="Dune", price=19.99, stock_quantity=8, author_id=herbert.id, supplier_id=supplier2.id)
        session.add_all([book1, book2, book3])
        session.flush()

        # Catégories des livres
        book1.categories = [sf, pol]
        book2.categories = [pol, roman]
        book3.categories = [sf, roman]

        # Clients
        from models.customer import Customer
        alice = Customer(name="Alice Dupont", email="alice@example.com")
        bob = Customer(name="Bob Martin", email="bob@example.com")
        session.add_all([alice, bob])

        session.commit()
        print("✅ Seed terminé avec succès !")

    except Exception as e:
        session.rollback()
        print(f"❌ Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()