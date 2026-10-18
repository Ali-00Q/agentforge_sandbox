from typing import Annotated
from fastapi import APIRouter, Query
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["products"])


class Product(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    category: str | None = None
    in_stock: bool = True


PRODUCTS: list[Product] = [
    Product(
        id=1,
        name="Laptop",
        description="High performance laptop",
        price=999.99,
        category="Electronics",
        in_stock=True,
    ),
    Product(
        id=2,
        name="Wireless Mouse",
        description="Ergonomic optical mouse",
        price=29.99,
        category="Electronics",
        in_stock=True,
    ),
    Product(
        id=3,
        name="Coffee Mug",
        description="Ceramic mug 350ml",
        price=12.50,
        category="Home & Kitchen",
        in_stock=True,
    ),
    Product(
        id=4,
        name="Notebook",
        description="Grid lined hardcover notebook",
        price=8.99,
        category="Stationery",
        in_stock=False,
    ),
]


@router.get("/", response_model=list[Product])
def list_products(
    category: Annotated[str | None, Query(description="Filter by product category")] = None,
    search: Annotated[str | None, Query(description="Search by product name")] = None,
) -> list[Product]:
    products = PRODUCTS
    if category:
        products = [p for p in products if p.category and p.category.lower() == category.lower()]
    if search:
        products = [p for p in products if search.lower() in p.name.lower()]
    return products
