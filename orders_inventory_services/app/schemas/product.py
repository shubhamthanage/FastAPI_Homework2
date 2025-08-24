# app/schemas/product.py
from typing import Optional
from pydantic import BaseModel, Field, condecimal, conint

class ProductBase(BaseModel):
    sku: str = Field(..., example="SKU-1234")
    name: str = Field(..., example="Example product")
    price: float = Field(..., gt=0, example=9.99)
    stock: int = Field(..., ge=0, example=10)

class ProductCreate(ProductBase):
    pass

class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    # allow partial updates
    sku: Optional[str] = None
    name: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)