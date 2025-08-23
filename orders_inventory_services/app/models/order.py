# app/models/order.py
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column, Enum, Integer, ForeignKey
import enum

class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    CANCELED = "CANCELED"

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(sa_column=Column(Integer), nullable=False)
    status: OrderStatus = Field(default=OrderStatus.PENDING, sa_column=Column(Enum(OrderStatus), nullable=False))
    created_at: datetime = Field(default_factory=datetime.utcnow)