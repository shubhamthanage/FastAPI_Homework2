# app/api/v1/endpoints/products.py
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session
from orders_inventory_services.app.db.session import get_session
from orders_inventory_services.app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from orders_inventory_services.app.services.product_service import create_product, get_product, list_products, update_product, delete_product

router = APIRouter()

@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create(p: ProductCreate, session: Session = Depends(get_session)):
    try:
        return create_product(session, p)
    except ValueError as e:
        # duplicate SKU or validation
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("", response_model=List[ProductRead])
def list_all(session: Session = Depends(get_session)):
    # For a small sample app we don't page; if large datasets, add pagination.
    return list_products(session)

@router.get("/{product_id}", response_model=ProductRead)
def get_one(product_id: int, session: Session = Depends(get_session)):
    prod = get_product(session, product_id)
    if not prod:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return prod

@router.put("/{product_id}", response_model=ProductRead)
def put(product_id: int, p: ProductUpdate, session: Session = Depends(get_session)):
    try:
        updated = update_product(session, product_id, p)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(product_id: int, session: Session = Depends(get_session)):
    try:
        delete_product(session, product_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return None