from fastapi import FastAPI
from app.db.database import create_start_app_handler, create_stop_app_handler
from app.routes import user_routes, product_routes, sale_routes, transaction_routes
from app.routes.auth import router as auth_router
import logging

app = FastAPI()

app.add_event_handler("startup", create_start_app_handler(app))
app.add_event_handler("shutdown", create_stop_app_handler(app))

app.include_router(user_routes.router, prefix="/api/v1", tags=["users"])
app.include_router(product_routes.router, prefix="/api/v1", tags=["products"])
app.include_router(sale_routes.router, prefix="/api/v1", tags=["sales"])
app.include_router(transaction_routes.router, prefix="/api/v1", tags=["transactions"])
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])