from database.db import SessionLocal
from models.author import Author
from models.supplier import Supplier
from models.category import Category
from models.book import Book
from models.customer import Customer
from models.order import Order, OrderLine
from controllers.order_controller import OrderController
from services.stock_service import restock
import pprint

def main():
    session = SessionLocal()
    try:
        # ── Récupérer des données existantes ──────────────────
        alice = session.get(Customer, 1)
        book1 = session.get(Book, 1)
        book2 = session.get(Book, 2)

        print(f"\n👤 Client : {alice.name}")
        print(f"📖 Livre 1 : {book1.title} — stock : {book1.stock_quantity}")
        print(f"📖 Livre 2 : {book2.title} — stock : {book2.stock_quantity}")

        # ── Créer une commande ────────────────────────────────
        order = OrderController.create_draft(session, customer_id=alice.id)
        print(f"\n📋 Commande créée — statut : {order.status.value}")

        # ── Ajouter des lignes ────────────────────────────────
        OrderController.add_line(session, order, book_id=book1.id, quantity=2)
        OrderController.add_line(session, order, book_id=book2.id, quantity=1)
        print(f"➕ Lignes ajoutées")

        # ── Confirmer la commande ─────────────────────────────
        OrderController.confirm(session, order)
        session.flush()
        print(f"\n✅ Commande confirmée — statut : {order.status.value}")
        print(f"📦 Stock {book1.title} après confirmation : {book1.stock_quantity}")
        print(f"📦 Stock {book2.title} après confirmation : {book2.stock_quantity}")

        # ── Clôturer la commande ──────────────────────────────
        OrderController.close(session, order)
        print(f"\n🏁 Commande clôturée — statut : {order.status.value}")

        # ── Afficher le résumé ────────────────────────────────
        print(f"\n📊 Résumé de la commande :")
        pprint.pprint(OrderController.summary(order))

        # ── Réapprovisionner ──────────────────────────────────
        restock(session, book1.id, qty=5)
        print(f"\n📦 Réapprovisionnement {book1.title} — nouveau stock : {book1.stock_quantity}")

        session.commit()
        print("\n✔ Toutes les opérations ont été persistées en base.\n")

    except Exception as e:
        session.rollback()
        print(f"\n❌ Erreur : {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    main()