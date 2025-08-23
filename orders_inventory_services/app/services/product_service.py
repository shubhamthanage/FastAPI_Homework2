# app/services/product_service.py
from sqlmodel import Session, select
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

def create_product(session: Session, p: ProductCreate) -> Product:
    # check duplicate SKU
    existing = session.exec(select(Product).where(Product.sku == p.sku)).first()
    if existing:
        raise ValueError("SKU already exists")
    prod = Product(sku=p.sku, name=p.name, price=p.price, stock=p.stock)
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod

def list_products(session: Session):
    return session.exec(select(Product)).all()

def get_product(session: Session, product_id: int):
    return session.get(Product, product_id)

def update_product(session: Session, product_id: int, p: ProductUpdate):
    prod = session.get(Product, product_id)
    if not prod:
        raise KeyError("Not found")
    if p.sku and p.sku != prod.sku:
        # ensure new SKU not used
        other = session.exec(select(Product).where(Product.sku == p.sku)).first()
        if other:
            raise ValueError("SKU already exists")
        prod.sku = p.sku
    if p.name is not None:
        prod.name = p.name
    if p.price is not None:
        if p.price <= 0:
            raise ValueError("price must be > 0")
        prod.price = p.price
    if p.stock is not None:
        if p.stock < 0:
            raise ValueError("stock must be >= 0")
        prod.stock = p.stock
    session.add(prod)
    session.commit()
    session.refresh(prod)
    return prod

def delete_product(session: Session, product_id: int):
    prod = session.get(Product, product_id)
    if not prod:
        raise KeyError("Not found")
    session.delete(prod)
    session.commit()