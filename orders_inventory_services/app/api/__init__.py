# app/api/__init__.py
from fastapi import APIRouter
from orders_inventory_services.app.api.v1.endpoints import products, orders, payments

api_router = APIRouter()
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(payments.router, prefix="/webhooks", tags=["payments"])