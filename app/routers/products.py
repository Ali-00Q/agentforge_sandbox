from typing import Annotated
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field

router = APIRouter(prefix="/products", tags=["products"])


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float = Field(gt=0)
    in_stock: bool = True


PRODUCTS_DB: list[Product] = [
    Product(id=1, name="Laptop", description="High performance laptop", price=999.99, in_stock=True),
    Product(id=2, name="Wireless Mouse", description="Ergonomic optical mouse", price=29.99, in_stock=True),
    Product(id=3, name="Keyboard", description="Mechanical RGB keyboard", price=79.99, in_stock=False),
]


@router.get("/", response_model=list[Product])
def get_products(
    q: Annotated[str | None, Query(description="Search products by name")] = None,
) -> list[Product]:
    if q:
        return [p for p in PRODUCTS_DB if q.lower() in p.name.lower()]
    return PRODUCTS_DB
