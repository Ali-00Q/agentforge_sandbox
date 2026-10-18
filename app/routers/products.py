from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    in_stock: bool = True


PRODUCTS: list[Product] = [
    Product(id=1, name="Laptop", description="High performance laptop", price=999.99, in_stock=True),
    Product(id=2, name="Mouse", description="Wireless optical mouse", price=29.99, in_stock=True),
    Product(id=3, name="Keyboard", description="Mechanical RGB keyboard", price=79.99, in_stock=False),
]


@router.get("/")
def list_products(
    q: Annotated[str | None, Query(description="Search filter by name")] = None,
) -> list[Product]:
    if q:
        term = q.lower()
        return [p for p in PRODUCTS if term in p.name.lower()]
    return PRODUCTS


@router.get("/{product_id}")
def get_product(product_id: int) -> Product:
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
