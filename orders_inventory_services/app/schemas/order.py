# app/schemas/order.py
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from orders_inventory_services.app.models.order import OrderStatus

class OrderCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class OrderRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: OrderStatus
    created_at: datetime

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    # allow only status changes (and maybe quantity before PAID)
    status: Optional[OrderStatus] = None
    quantity: Optional[int] = Field(None, gt=0)