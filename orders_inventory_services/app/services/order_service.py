# app/services/order_service.py
from sqlmodel import Session, select
from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.schemas.order import OrderCreate, OrderUpdate
from datetime import datetime

def create_order(session: Session, o: OrderCreate) -> Order:
    # atomic-ish transaction: check stock, decrement, create order
    product = session.get(Product, o.product_id)
    if not product:
        raise ValueError("Product not found")
    if o.quantity <= 0:
        raise ValueError("Quantity must be > 0")
    if product.stock < o.quantity:
        raise ValueError("Insufficient stock")
    # reduce stock and create order
    product.stock -= o.quantity
    order = Order(product_id=o.product_id, quantity=o.quantity, status=OrderStatus.PENDING)
    session.add(product)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_order(session: Session, order_id: int):
    return session.get(Order, order_id)

def update_order(session: Session, order_id: int, payload: OrderUpdate):
    order = session.get(Order, order_id)
    if not order:
        raise KeyError("Order not found")
    # quantity allowed only when PENDING
    if payload.quantity is not None:
        if order.status != OrderStatus.PENDING:
            raise ValueError("Cannot change quantity unless order is PENDING")
        if payload.quantity <= 0:
            raise ValueError("Quantity must be > 0")
        # check stock delta
        product = session.get(Product, order.product_id)
        delta = payload.quantity - order.quantity
        if delta > 0 and product.stock < delta:
            raise ValueError("Insufficient stock to increase quantity")
        product.stock -= delta
        order.quantity = payload.quantity
        session.add(product)
    if payload.status is not None:
        # simple allowed transitions
        allowed = {
            OrderStatus.PENDING: {OrderStatus.PAID, OrderStatus.CANCELED},
            OrderStatus.PAID: {OrderStatus.SHIPPED, OrderStatus.CANCELED},
            OrderStatus.SHIPPED: set(),
            OrderStatus.CANCELED: set(),
        }
        if payload.status == order.status:
            pass
        elif payload.status in allowed[order.status]:
            order.status = payload.status
        else:
            raise ValueError(f"Invalid status transition from {order.status} to {payload.status}")
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def delete_order(session: Session, order_id: int):
    order = session.get(Order, order_id)
    if not order:
        raise KeyError("Not found")
    # semantics: physical deletion allowed only for PENDING orders; otherwise recommend cancel
    if order.status != OrderStatus.PENDING:
        raise ValueError("Only PENDING orders can be deleted; use cancel for others")
    # return stock
    product = session.get(Product, order.product_id)
    product.stock += order.quantity
    session.add(product)
    session.delete(order)
    session.commit()