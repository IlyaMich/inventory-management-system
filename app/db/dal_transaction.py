from app.db.dal_generic import DALGeneric
from app.models.transaction import Transaction

class DALTransaction(DALGeneric):
    def __init__(self, db):
        super().__init__(model=Transaction, collection=db["transactions"])