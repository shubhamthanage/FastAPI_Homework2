# app/models/product.py
from typing import Optional
from sqlmodel import SQLModel, Field, Column, String, Float, Integer
from sqlalchemy import Index

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sku: str = Field(sa_column=Column("sku", String, unique=True, index=True), nullable=False)
    name: str
    price: float = Field(sa_column=Column(Float), nullable=False)
    stock: int = Field(default=0, sa_column=Column(Integer), nullable=False)

# Index already applied via sa_column(index=True), additional indexes can be added if needed