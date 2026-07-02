# Mini ERP

Mini ERP style librairie, développé en Python avec une architecture MVC complète.

## Stack technique

- **Python** — langage principal
- **PostgreSQL** — base de données relationnelle
- **SQLAlchemy 2.0** — ORM
- **Alembic** — migrations
- **FastAPI** — API REST
- **React + Vite** — frontend

## Architecture
mini_erp/
├── models/          # Entités SQLAlchemy
├── repositories/    # Accès base de données
├── services/        # Logique métier
├── controllers/     # Orchestration
├── api/routers/     # Routes FastAPI
└── migrations/      # Migrations Alembic

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/demainwilliam-spec/mini_erp.git
cd mini_erp
```

### 2. Créer l'environnement virtuel

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configurer les variables d'environnement

```bash
cp .env.example .env
# Modifie .env avec ton mot de passe PostgreSQL
```

### 5. Créer la base de données

Dans pgAdmin, crée une base de données `mini_erp`.

### 6. Lancer les migrations

```bash
python -m alembic upgrade head
```

### 7. Insérer les données de test

```bash
python seed.py
```

### 8. Lancer l'API

```bash
uvicorn api.main:app --reload
```

L'API est accessible sur **http://localhost:8000**
La documentation interactive sur **http://localhost:8000/docs**

### 9. Lancer le frontend

```bash
cd ../mini_erp_front
npm install
npm run dev
```

Le frontend est accessible sur **http://localhost:5173**

## Entités

| Entité | Description |
|---|---|
| Author | Auteurs des livres |
| Supplier | Fournisseurs |
| Book | Livres (entité centrale) |
| Category | Catégories (relation N↔N avec Book) |
| Customer | Clients |
| Order | Commandes (draft → confirmed → closed) |
| OrderLine | Lignes de commande |
| StockMovement | Historique des mouvements de stock |

## Flux métier
Créer commande (draft)
→ Ajouter des lignes
→ Confirmer (stock décrémenté automatiquement)
→ Clôturer