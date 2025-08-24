# app/api/v1/endpoints/orders.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from orders_inventory_services.app.db.session import get_session
from orders_inventory_services.app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from orders_inventory_services.app.services.order_service import create_order, get_order, update_order, delete_order

router = APIRouter()

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
def post_order(o: OrderCreate, session: Session = Depends(get_session)):
    try:
        return create_order(session, o)
    except ValueError as e:
        # e.g., insufficient stock or invalid product
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.get("/{order_id}", response_model=OrderRead)
def get_one(order_id: int, session: Session = Depends(get_session)):
    order = get_order(session, order_id)
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order

@router.put("/{order_id}", response_model=OrderRead)
def put(order_id: int, payload: OrderUpdate, session: Session = Depends(get_session)):
    try:
        return update_order(session, order_id, payload)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        # invalid state transition
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(order_id: int, session: Session = Depends(get_session)):
    try:
        delete_order(session, order_id)
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return None