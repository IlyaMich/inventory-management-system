from app.db.dal_product import DALProduct
from app.db.dal_user import DALUser
from app.db.dal_sale import DALSale
from app.db.dal_transaction import DALTransaction
from app.db.database import get_database

database_name = "inventory-mng-local"

def get_dal_product():
    db = get_database(database_name)
    return DALProduct(db)

def get_dal_user():
    db = get_database(database_name)
    return DALUser(db)

def get_dal_sale():
    db = get_database(database_name)
    return DALSale(db)

def get_dal_transaction():
    db = get_database(database_name)
    return DALTransaction(db)