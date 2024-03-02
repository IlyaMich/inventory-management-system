from app.db.dal_generic import DALGeneric
from app.models.product import Product

class DALProduct(DALGeneric):
    def __init__(self, db):
        super().__init__(model=Product, collection=db["products"])
