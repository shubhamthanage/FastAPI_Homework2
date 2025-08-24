# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel
from orders_inventory_services.app.db.session import engine
from orders_inventory_services.app.api.v1 import api_router
from orders_inventory_services.app.core.config import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # create DB tables on startup
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Orders & Inventory Service",
    version="0.1.0",
    description="A tiny Orders & Inventory microservice with product CRUD, orders, and payment webhook.",
    openapi_tags=[
        {"name": "products", "description": "Product CRUD operations"},
        {"name": "orders", "description": "Order creation and tracking"},
        {"name": "payments", "description": "Payment webhooks"},
    ],
    lifespan=lifespan,
)

# CORS for testing from other hosts (adjust for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")