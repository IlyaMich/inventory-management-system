from app.db.dal_generic import DALGeneric
from app.models.sale import Sale

class DALSale(DALGeneric):
    def __init__(self, db):
        super().__init__(model=Sale, collection=db["sales"])
